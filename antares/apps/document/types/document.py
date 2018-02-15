from datetime import datetime
import logging
import uuid
import hashlib

from dateutil import parser as dateparser
from django.utils import timezone
from django.utils.translation import ugettext as _
import js2py
from lxml import etree
from lxml import objectify

from antares.apps.accounting.models import AccountType
from antares.apps.client.models.client import Client
from antares.apps.client.models.client_branch import ClientBranch
from antares.apps.core.constants import FieldDataType
from antares.apps.core.constants import HrnModuleType, ScriptEngineType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import ConceptType
from antares.apps.core.models import HrnCode
from antares.apps.flow.models import FlowCase
from antares.apps.user.models import User
from antares.apps.obligation.models import ObligationVector

from ..constants import DocumentEventType, FormClassType
from ..constants import DocumentStatusType, DocumentOriginType, DocumentAssociationType
from ..constants import FormDefinitionStatusType
from ..exceptions import DocumentDoesNotExistException
from ..exceptions import DocumentStatusException, InvalidDocumentValueException
from ..exceptions import FormDefinitionNotFoundException, FormDefintionIsNotActiveException
from ..exceptions import InvalidDocumentStatusException, DocumentFieldNotFound
from ..models import DocumentHeader, DocumentField, IndexedField
from ..models import FormDefinition
from antares.apps.flow.models.operation.flow_activity import FlowActivity
from prompt_toolkit.key_binding.bindings.named_commands import self_insert
from antares.apps.document.exceptions.document_validation_exception import DocumentValidationException
from antares.apps.document.exceptions.document_required_exception import DocumentRequiredException
from typing import Dict

logger = logging.getLogger(__name__)


class Document(object):
    """ Contains and manages a Document entity
    
    """

    IMMUTABLE_HEADER_FIELDS = [
        'document_id',
        'form_version',
        'form_name',
    ]

    def __init__(self, *args, **kwargs):
        """ Creates or loads a document. 
        
        To create a document, the call would be document = new Document(form_id=<<form_id>>) and to load a document 
        the call would be document = new Document(document_id=<<document_id>>) 
        
        """
        self.fields = {}
        self.header_fields = {}
        self.document_xml = None
        self.header = None
        self.document_id = 0

        if kwargs.get('document_id') is not None:
            self._init_with_id(kwargs.get('document_id'))
        elif kwargs.get('form_id') is not None:
            if (kwargs.get('header_fields_dict') is None):
                self._init_with_form_id(kwargs.get('form_id'))
            else:
                self._init_with_form_id(
                    kwargs.get('form_id'), kwargs.get('header_fields_dict'))
        else:
            raise ValueError(__name__ + ".exceptions.couldnt_create_document")

    def _init_with_id(self, document_id: str):
        """ Instantiates a document instance based on the document id

        :param document_id: The document ID, which has to exist on the database
        :returns: the document instance
        """
        if isinstance(document_id, uuid.UUID):
            document_uuid = document_id
        else:
            document_uuid = uuid.UUID(document_id)
        self.header = DocumentHeader.find_one(document_uuid)
        if self.header is None:
            raise DocumentDoesNotExistException(
                _(__name__ + ".document_does_exist {document_id}".format(
                    document_id=document_id)))
        self.document_id = self.header.id

        logger.debug("************** " + _(
            __name__ + ".messages.document_load") + " ******************")
        logger.debug(
            _(__name__ + ".messages.document_load_document_id {document_id}")
            .format(document_id=self.document_id))
        logger.debug("************** ***************** **************")
        logger.debug("************** ***************** **************")
        logger.debug("************** ***************** **************")

        self.document_xml = etree.fromstring(
            self.header.form_definition.definition)
        self.document_xml = FormDefinition.set_blank_header_xml(
            self.document_xml)
        self._hydrate_document()
        self._evaluate_field_calculation()
        self._process_external_function_events(
            DocumentEventType.DRAFT_MODIFICATION)

    def _init_with_form_id(self,
                           form_id: str,
                           header_fields_dict: Dict[str, str] = None):
        """ Instantiates a document instance based on the document id

        :param document_id: The document ID, which has to exist on the database
        :returns: the document instance
        """

        form_definition = FormDefinition.find_one(form_id)
        if form_definition is None:
            raise FormDefinitionNotFoundException(
                _(__name__ + ".exceptions.form_was_not_found"))
        if form_definition.status == FormDefinitionStatusType.DEACTIVATED:
            raise FormDefintionIsNotActiveException(
                _(__name__ + ".exceptions.form_is_not_active"))

        self.document_xml = etree.fromstring(form_definition.definition)
        self.document_xml = FormDefinition.set_blank_header_xml(
            self.document_xml)

        self.header = DocumentHeader()
        self.header.form_definition = form_definition
        self.header.status = DocumentStatusType.DRAFTED
        self.header.draft_date = timezone.now()
        self.header.association_type = DocumentAssociationType.NONE
        self.header.creation_date = timezone.now()
        self.header.active_version = True
        self.header.origin = DocumentOriginType.UNKNOWN
        self.header.document_version = 0
        self.header.hash = ""
        self.header.save()

        self.document_id = self.header.id

        self._hydrate_document()
        self._evaluate_field_calculation()
        logger.debug("************** " + _(
            __name__ + ".messages.document_load") + " ******************")
        logger.debug(
            _(__name__ + ".messages.document_load_document_id {document_id}")
            .format(document_id=self.document_id))
        logger.debug("************** ***************** **************")
        logger.debug("************** ***************** **************")
        logger.debug("************** ***************** **************")

        if form_definition.form_class.type == FormClassType.OBLIGATION_BASED:
            if form_definition.form_class.concept_type is not None:
                self.set_header_field('concept_type',
                                      form_definition.form_class.concept_type)
        if form_definition.form_class.account_type is not None:
            self.set_header_field('account_type',
                                  form_definition.form_class.account_type)

        if (header_fields_dict is not None):
            self.set_header_fields(header_fields_dict)
        self._map_header_fields_to_fields()
        self._process_field_sources()
        self._evaluate_field_calculation()
        self._process_functions(DocumentEventType.CREATION)
        self._process_hrn_script(DocumentEventType.CREATION)
        self._map_fields_to_header_fields()
        self._hibernate_document()

    def _hydrate_document(self):
        """ Sets all the values on the database on the XML object
        
        """
        self._hydrate_header()
        self._hydrate_body()
        self._process_field_sources()

    def _hydrate_header(self):
        """ Sets the header fields onto the XML object
        
        """
        headerElements = self.document_xml.find('headerElements')
        accountingElements = headerElements.find('accountingElements')

        if accountingElements is not None:
            if self.header.account_document is not None:
                base_document = accountingElements.find('baseDocument')
                base_document.text = str(self.header.account_document)
            if self.header.concept_type is not None:
                concept_type = accountingElements.find('conceptType')
                concept_type.text = str(self.header.concept_type.id)
            if self.header.client is not None:
                client = accountingElements.find('client')
                client.text = str(self.header.client.id)
            if self.header.branch is not None:
                client = accountingElements.find('branch')
                client.text = str(self.header.branch.id)
            if self.header.period is not None:
                period = accountingElements.find('period')
                period.text = str(self.header.period)
            if self.header.account_type is not None:
                account_type = accountingElements.find('accountType')
                account_type.text = self.header.account_type.id
            if self.header.active_version:
                active_version = headerElements.find('activeVersion')
                active_version.text = "yes"
            else:
                active_version.text = "no"
            if self.header.associated_to is not None:
                associated_to = headerElements.find('associatedTo')
                associated_to.text = str(self.header.associated_to)
            if self.header.association_type is not None:
                association_type = headerElements.find('associationType')
                association_type.text = self.header.association_type.value
            if self.header.creation_date is not None:
                creation_date = headerElements.find('creationDate')
                creation_date.text = self.header.creation_date.isoformat()
            if self.header.draft_date is not None:
                draft_date = headerElements.find('draftDate')
                draft_date.text = self.header.draft_date.isoformat()
            if self.header.delete_case is not None:
                delete_case = headerElements.find('deleteCase')
                delete_case.text = str(self.header.delete_case.id)
            if self.header.id is not None:
                self.document_xml.set('documentId', str(self.header.id))
                self.document_xml.set('formDefinition',
                                      str(self.header.form_definition.id))
            if self.header.document_version is not None:
                document_version = headerElements.find('documentVersion')
                document_version.text = str(self.header.document_version)
            if self.header.status is not None:
                status = headerElements.find('status')
                status.text = self.header.status.value
            if self.header.hash is not None:
                doc_hash = headerElements.find('hash')
                doc_hash.text = self.header.hash
            if self.header.origin is not None:
                origin = headerElements.find('origin')
                origin.text = self.header.origin.value
            if self.header.save_date is not None:
                save_date = headerElements.find('saveDate')
                save_date.text = self.header.save_date.isoformat()
            if self.header.author is not None:
                author = headerElements.find('author')
                author.text = str(self.header.author.id)
                author_name = headerElements.find('authorName')
                try:
                    author_name.text = self.header.author.client.full_name
                except:
                    author_name.text = None
            if self.header.hrn_code is not None:
                hrn_code = headerElements.find('hrnCode')
                hrn_code.text = self.header.hrn_code
            if self.header.hrn_title is not None:
                hrn_title = headerElements.find('hrnTitle')
                hrn_title.text = self.header.hrn_title
            if self.header.secondary_client is not None:
                secondary_client = headerElements.find('secondaryClient')
                secondary_client.text = str(self.header.secondary_client.id)

    def _hydrate_body(self):
        for page in self.document_xml.iterfind('structuredData/page'):
            for line in page.iterfind('line'):
                for field in line.iterfind('field'):
                    if (field.get('id') is not None
                            and field.get('dataType') is not None
                            and field.get('type') is not None
                            and field.get('type').lower() != 'label'):
                        fieldDb = DocumentField.find_one(
                            self.header, field.attrib['id'])
                        datatype = FieldDataType.to_enum(
                            field.attrib['dataType'])
                        if fieldDb is not None:
                            if datatype == FieldDataType.INTEGER:
                                if fieldDb.integer_value is not None:
                                    field.text = str(fieldDb.integer_value)
                            elif datatype == FieldDataType.FLOAT:
                                if fieldDb.float_value is not None:
                                    field.text = str(fieldDb.float_value)
                            elif datatype == FieldDataType.STRING:
                                if fieldDb.string_value is not None:
                                    field.text = fieldDb.string_value
                            elif datatype == FieldDataType.TEXT:
                                if fieldDb.text_value is not None:
                                    field.text = fieldDb.text_value
                            elif datatype == FieldDataType.DATE:
                                if fieldDb.date_value is not None:
                                    field.text = fieldDb.date_value.isoformat()
                            elif datatype == FieldDataType.DATETIME:
                                if fieldDb.date_value is not None:
                                    field.text = fieldDb.date_value.isoformat()
                            elif datatype == FieldDataType.UUID:
                                if fieldDb.uuid_value is not None:
                                    field.text = fieldDb.uuid_value
                            elif datatype == FieldDataType.CLIENT:
                                if fieldDb.uuid_value is not None:
                                    client_obj = Client.find_one(fieldDb.uuid_value)
                                    field.text = str(client_obj.id)
                                    field.attrib['displayValue'] = str(client_obj)
                            elif datatype == FieldDataType.USER:
                                if fieldDb.uuid_value is not None:
                                    user_obj = User.find_one(fieldDb.uuid_value)
                                    field.text = str(user_obj.id)
                                    field.attrib['displayValue'] = str(user_obj)
                            elif datatype == FieldDataType.DOCUMENT:
                                if fieldDb.uuid_value is not None:
                                    document_obj = Document(document_id=fieldDb.uuid_value) 
                                    field.text = str(document_obj.id)
                                    if(document_obj.header.hrn_code is not None):
                                        field.attrib['displayValue'] = document_obj.header.hrn_code
                            else:
                                raise NotImplementedError(
                                    _(__name__ +
                                      ".messages.field_type_not_implemented_yet"
                                      ))

    def _hibernate_document(self):
        self._hibernate_header()
        self._hibernate_fields()
        self.header.save()

    def _hibernate_header(self):
        headerElements = self.document_xml.find('headerElements')
        accountingElements = headerElements.find('accountingElements')

        base_document_node = accountingElements.find('baseDocument')
        if (base_document_node is not None and base_document_node.text):
            try:
                document = Document(uuid.UUID(base_document_node.text))
            except ValueError:
                document = None
            if (document is not None):
                self.header.account_base_document = document.header
        period_node = accountingElements.find('period')
        if (period_node is not None and period_node.text
                and period_node.text != ''):
            self.header.period = int(float(period_node.text))

        concept_type_node = accountingElements.find('conceptType')
        if (concept_type_node is not None and concept_type_node.text):
            try:
                concept_type = ConceptType.find_one(
                    uuid.UUID(concept_type_node.text))
            except ValueError:
                concept_type = None
            if (concept_type is not None):
                self.header.concept_type = concept_type

        client_node = accountingElements.find('client')
        if (client_node is not None and client_node.text):
            try:
                client = Client.find_one(uuid.UUID(client_node.text))
            except ValueError:
                client = None
            if (client is not None):
                self.header.client = client

        branch_node = accountingElements.find('branch')
        if (branch_node is not None and branch_node.text):
            try:
                branch = ClientBranch.find_one(uuid.UUID(branch_node.text))
            except ValueError:
                branch = None
            if (branch is not None):
                self.header.branch = branch

        account_type_node = accountingElements.find('accountType')
        if (account_type_node is not None and account_type_node.text):
            try:
                account_type = AccountType.find_one(
                    uuid.UUID(account_type_node.text))
            except ValueError:
                account_type = None
            if (account_type is not None):
                self.header.account_type = account_type

        active_version_node = headerElements.find('activeVersion')
        if (active_version_node is not None and active_version_node.text):
            if (active_version_node.text.lower() == 'yes'
                    or active_version_node.text.lower() == 'true'):
                self.header.active_version = True
            else:
                self.header.active_version = False

        associated_to_node = headerElements.find('associatedTo')
        if (associated_to_node is not None and associated_to_node.text):
            try:
                associated_document = Document(
                    uuid.UUID(associated_to_node.text))
            except ValueError:
                associated_document = None
            if (associated_document is not None):
                self.header.associated_to = associated_document

        association_type_node = headerElements.find('associationType')
        if (association_type_node is not None and association_type_node.text):
            self.header.association_type = DocumentAssociationType.to_enum(
                association_type_node.text)

        creation_date_node = headerElements.find('creationDate')
        if (creation_date_node is not None and creation_date_node.text):
            try:
                self.header.creation_date = dateparser.parse(
                    creation_date_node.text)
            except ValueError:
                pass

        draft_date_node = headerElements.find('draftDate')
        if (draft_date_node is not None and draft_date_node.text):
            try:
                self.header.draft_date = dateparser.parse(draft_date_node.text)
            except ValueError:
                pass
        delete_case_node = headerElements.find('deleteCase')
        if (delete_case_node is not None and delete_case_node.text):
            try:
                self.header.delete_case = FlowCase.find_one(
                    uuid.UUID(delete_case_node))
            except ValueError:
                pass

        related_case_node = headerElements.find('relatedCase')
        if (related_case_node is not None and related_case_node.text):
            try:
                self.header.related_case = FlowCase.find_one(
                    uuid.UUID(related_case_node.text))
            except ValueError:
                pass
        status_node = headerElements.find('status')
        if (status_node is not None and status_node.text):
            self.header.status = DocumentStatusType.to_enum(status_node.text)

        document_version_node = headerElements.find('documentVersion')
        if (document_version_node is not None and document_version_node.text):
            try:
                self.header.document_version = int(
                    float(document_version_node.text))
            except ValueError:
                pass
        document_hash_node = headerElements.find('hash')
        if (document_hash_node is not None and document_hash_node.text):
            self.header.hash = document_hash_node.text

        origin_node = headerElements.find('origin')
        if (origin_node is not None and origin_node.text):
            self.header.origin = DocumentOriginType.to_enum(origin_node.text)

        save_date_node = headerElements.find('saveDate')
        if (save_date_node is not None and save_date_node.text):
            try:
                self.header.save_date = dateparser.parse(save_date_node.text)
            except ValueError:
                pass

        author_node = headerElements.find('author')
        if (author_node is not None and author_node.text):
            self.header.author = User.find_one(author_node.text)

        hrn_code_node = headerElements.find('hrnCode')
        if (hrn_code_node is not None and hrn_code_node.text):
            self.header.hrn_code = hrn_code_node.text

        hrn_title_node = headerElements.find('hrnTitle')
        if (hrn_title_node is not None and hrn_title_node.text):
            self.header.hrn_title = hrn_title_node.text

        secondary_client_node = headerElements.find('secondaryClient')
        if (secondary_client_node is not None and secondary_client_node.text):
            try:
                secondary_client = Client.find_one(
                    uuid.UUID(secondary_client_node.text))
            except ValueError:
                pass
            if (secondary_client is not None):
                self.header.secondary_client = secondary_client

    def _hibernate_fields(self):
        for page in self.document_xml.iterfind('structuredData/page'):
            for line in page.iterfind('line'):
                for field in line.iterfind('field'):
                    if (field.get('id') is not None
                            and field.get('dataType') is not None
                            and field.get('type') is not None
                            and field.get('type').lower() != 'label'):
                        datatype = FieldDataType.to_enum(field.get('dataType'))
                        fieldDb = DocumentField.find_one(
                            self.header, field.get('id'))
                        indexedDb = IndexedField.find_one(
                            self.header, field.get('id'))
                        if field.text is not None:
                            if datatype == FieldDataType.STRING:
                                if (fieldDb is not None and
                                        fieldDb.string_value != field.text):
                                    fieldDb.string_value = field.text
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.string_value = field.text
                                    fieldDb.data_type = str(
                                        FieldDataType.STRING)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and indexedDb.string_value !=
                                            field.text):
                                        indexedDb.string_value = field.text
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.string_value = field.text
                                        indexedDb.data_type = str(
                                            FieldDataType.STRING)
                                        indexedDb.save()
                            elif datatype == FieldDataType.TEXT:
                                if (fieldDb is not None
                                        and fieldDb.text_value != field.text):
                                    fieldDb.text_value = field.text
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.text_value = field.text
                                    fieldDb.data_type = str(FieldDataType.TEXT)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and indexedDb.text_value !=
                                            field.text):
                                        indexedDb.text_value = field.text
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.text_value = field.text
                                        indexedDb.data_type = str(
                                            FieldDataType.TEXT)
                                        indexedDb.save()
                            elif datatype == FieldDataType.INTEGER:
                                if (fieldDb is not None and
                                        fieldDb.string_value != field.text):
                                    fieldDb.integer_value = int(
                                        float(field.text))
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.integer_value = int(
                                            float(field.text))
                                    fieldDb.data_type = str(
                                        FieldDataType.INTEGER)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and indexedDb.integer_value !=
                                            field.text):
                                        indexedDb.integer_value = int(
                                            float(field.text))
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.integer_value = int(
                                                float(field.text))
                                        indexedDb.data_type = str(
                                            FieldDataType.INTEGER)
                                        indexedDb.save()
                            elif datatype == FieldDataType.FLOAT:
                                if (fieldDb is not None
                                        and fieldDb.float_value != field.text):
                                    fieldDb.float_value = float(field.text)
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.float_value = float(field.text)
                                    fieldDb.data_type = str(
                                        FieldDataType.FLOAT)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and indexedDb.float_value !=
                                            field.text):
                                        indexedDb.float_value = float(
                                            field.text)
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.float_value = float(
                                                field.text)
                                        indexedDb.data_type = str(
                                            FieldDataType.FLOAT)
                                        indexedDb.save()
                            elif datatype == FieldDataType.DATE:
                                #lets truncate and serialize it.
                                dt = dateparser.parse(field.text)
                                date_value = datetime(dt.year, dt.month,
                                                      dt.day)
                                if (fieldDb is not None
                                        and fieldDb.date_value != date_value):
                                    fieldDb.date_value = date_value
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (date_value is not None):
                                        fieldDb.date_value = date_value
                                    fieldDb.data_type = str(FieldDataType.DATE)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and indexedDb.date_value !=
                                            date_value):
                                        indexedDb.date_value = date_value
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.date_value = date_value
                                        indexedDb.data_type = str(
                                            FieldDataType.DATE)
                                        indexedDb.save()
                            elif datatype == FieldDataType.DATETIME:
                                #lets truncate and serialize it.
                                date_value = dateparser.parse(field.text)
                                if (fieldDb is not None
                                        and fieldDb.date_value != date_value):
                                    fieldDb.date_value = date_value
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.date_value = date_value
                                    fieldDb.data_type = str(FieldDataType.DATE)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and indexedDb.date_value !=
                                            date_value):
                                        indexedDb.date_value = date_value
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (date_value is not None):
                                            indexedDb.date_value = date_value
                                        indexedDb.data_type = str(
                                            FieldDataType.DATE)
                                        indexedDb.save()
                            elif datatype == FieldDataType.UUID:
                                if (fieldDb is not None
                                        and str(fieldDb.uuid_value) != str(
                                            field.text)):
                                    fieldDb.uuid_value = str(field.text)
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.uuid_value = str(field.text)
                                    fieldDb.data_type = str(FieldDataType.UUID)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and str(indexedDb.uuid_value) !=
                                            str(field.text)):
                                        indexedDb.uuid_value = str(field.text)
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.uuid_value = str(
                                                field.text)
                                        indexedDb.data_type = str(
                                            FieldDataType.UUID)
                                        indexedDb.save()
                            elif datatype == FieldDataType.CLIENT:
                                #This is an special case, we have to get first the proper object and then we serialize it as an UUID
                                client_obj = Client.find_one(field.text)
                                if (fieldDb is not None
                                        and str(fieldDb.uuid_value) != str(
                                            client_obj.id)):
                                    fieldDb.uuid_value = str(client_obj.id)
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.uuid_value = str(client_obj.id)
                                    fieldDb.data_type = str(
                                        FieldDataType.CLIENT)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and str(indexedDb.uuid_value) !=
                                            str(client_obj.id)):
                                        indexedDb.uuid_value = str(
                                            client_obj.id)
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.uuid_value = str(
                                                client_obj.id)
                                        indexedDb.data_type = str(
                                            FieldDataType.CLIENT)
                                        indexedDb.save()
                            elif datatype == FieldDataType.USER:
                                #This is an special case, we have to get first the proper object and then we serialize it as an UUID
                                user_obj = User.find_one(field.text)
                                if (fieldDb is not None
                                        and str(fieldDb.uuid_value) != str(
                                            user_obj.id)):
                                    fieldDb.uuid_value = str(user_obj.id)
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.uuid_value = str(user_obj.id)
                                    fieldDb.data_type = str(FieldDataType.USER)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and str(indexedDb.uuid_value) !=
                                            str(user_obj.id)):
                                        indexedDb.uuid_value = str(user_obj.id)
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.uuid_value = str(
                                                user_obj.id)
                                        indexedDb.data_type = str(
                                            FieldDataType.USER)
                                        indexedDb.save()
                            elif datatype == FieldDataType.DOCUMENT:
                                #This is an special case, we have to get first the proper 
                                # object and then we serialize it as an UUID
                                document_obj = Document(document_id = uuid(field.text))
                                if (fieldDb is not None
                                        and str(fieldDb.uuid_value) != str(
                                            document_obj.id)):
                                    fieldDb.uuid_value = str(document_obj.id)
                                    fieldDb.save()
                                elif (fieldDb is None):
                                    fieldDb = DocumentField()
                                    fieldDb.definition = field.get('id')
                                    fieldDb.document = self.header
                                    fieldDb.form_definition = self.header.form_definition
                                    if (field.text is not None):
                                        fieldDb.uuid_value = str(document_obj.id)
                                    fieldDb.data_type = str(
                                        FieldDataType.DOCUMENT)
                                    fieldDb.save()
                                if (field.get('indexed') and
                                    (field.get('indexed').lower() == 'true' or
                                     field.get('indexed').lower() == 'yes')):
                                    if (indexedDb is not None
                                            and str(indexedDb.uuid_value) !=
                                            str(document_obj.id)):
                                        indexedDb.uuid_value = str(
                                            document_obj.id)
                                        indexedDb.save()
                                    elif (indexedDb is None):
                                        indexedDb = IndexedField()
                                        indexedDb.definition = field.get('id')
                                        indexedDb.document = self.header
                                        indexedDb.form_definition = self.header.form_definition
                                        if (field.text is not None):
                                            indexedDb.uuid_value = str(
                                                document_obj.id)
                                        indexedDb.data_type = str(
                                            FieldDataType.DOCUMENT)
                                        indexedDb.save()

    def get_field_data_type(self, key: str) -> str:
        for page in self.document_xml.iterfind('structuredData/page'):
            for line in page.iterfind('line'):
                for field in line.iterfind('field'):
                    if (field.get('id') is not None
                            and field.get('dataType') is not None
                            and field.get('type') is not None
                            and field.get('id') == key
                            and field.get('type').lower() != 'label'):
                        return FieldDataType.to_enum(field.get('dataType'))
        raise DocumentFieldNotFound(
            _(__name__ + ".exceptions.document_field_not_found"))

    def get_field_source(self, key: str) -> str:
        for page in self.document_xml.iterfind('structuredData/page'):
            for line in page.iterfind('line'):
                for field in line.iterfind('field'):
                    if (field.get('id') is not None
                            and field.get('source') is not None
                            and field.get('type') is not None
                            and field.get('id') == key
                            and field.get('type').lower() != 'label'):
                        return field.get('source')
        raise DocumentFieldNotFound(
            _(__name__ + ".exceptions.document_field_not_found"))

    def get_field_value(self, key: str):
        for page in self.document_xml.iterfind('structuredData/page'):
            for line in page.iterfind('line'):
                for field in line.iterfind('field'):
                    if (field.get('id') is not None
                            and field.get('dataType') is not None
                            and field.get('type') is not None
                            and field.get('id') == key
                            and field.get('type').lower() != 'label'):
                        field_data_type = FieldDataType.to_enum(
                            field.get('dataType'))
                        if field_data_type == FieldDataType.CLIENT:
                            return Client.find_one(field.text)
                        if field_data_type == FieldDataType.UUID:
                            return uuid(field.text)
                        elif field_data_type == FieldDataType.USER:
                            return User.find_one(uuid(field.text))
                        elif field_data_type == FieldDataType.DOCUMENT:
                            return Document(document_id=uuid(field.text))
                        elif field_data_type == FieldDataType.INTEGER:
                            return int(float(field.text))
                        elif field_data_type == FieldDataType.FLOAT:
                            return float(field.text)
                        elif field_data_type == FieldDataType.DATE:
                            return dateparser.parse(field.text)
                        elif field_data_type == FieldDataType.DATETIME:
                            return dateparser.parse(field.text)
                        else:
                            return field.text

    def get_field_id_by_messagemap(self, message_map: str) -> str:
        """ Gets the id of the field based on the messageMap attribute or None if no key is found
            
            :param message_map: message key
            :returns: the field id
        """
        for page in self.document_xml.iterfind('structuredData/page'):
            for line in page.iterfind('line'):
                for field in line.iterfind('field'):
                    if (field.get('messageMap') is not None
                            and field.get('messageMap') == message_map
                            and field.get('type') is not None
                            and field.get('id') is not None
                            and field.get('type').lower() != 'label'):
                        return field.get('id')
        return None

    def set_field_value(self, key, value, display_value = None):
        for page in self.document_xml.iterfind('structuredData/page'):
            for line in page.iterfind('line'):
                for field in line.iterfind('field'):
                    if (field.get('id') is not None
                            and field.get('dataType') is not None
                            and field.get('type') is not None
                            and field.get('id') == key
                            and field.get('type').lower() != 'label'):
                        datatype = FieldDataType.to_enum(field.get('dataType'))
                        if datatype == FieldDataType.STRING:
                            field.text = value
                            return
                        elif datatype == FieldDataType.TEXT:
                            field.text = value
                            return
                        elif datatype == FieldDataType.INTEGER:
                            field.text = str(int(float(value)))
                            return
                        elif datatype == FieldDataType.FLOAT:
                            field.text = str(float(value))
                            return
                        elif datatype == FieldDataType.DATE:
                            try:
                                field.text = value.isoformat()
                            except:
                                pass
                            return
                        elif datatype == FieldDataType.UUID:
                            try:
                                field.text = str(value)
                            except:
                                pass
                            return
                        elif datatype == FieldDataType.BOOLEAN:
                            if (value == True):
                                field.text = 'yes'
                            elif (value == False):
                                field.text = 'no'
                            return
                        elif datatype == FieldDataType.USER:
                            if value != False:
                                if isinstance(value, str):
                                    value = User.find_one(uuid.UUID(value))
                                elif isinstance(value, uuid.UUID):
                                    value = User.find_one(value)
                                elif isinstance(value, User) == False:
                                    raise ValueError(
                                        _(__name__ +
                                          ".exceptions.user_field_does_not_understand_anything_but_User_objects"
                                          ))
                                field.text = str(value.id)
                            return
                        elif datatype == FieldDataType.DOCUMENT:
                            if value != False and value != "":
                                if isinstance(value, str) or isinstance(value, uuid):
                                    value = Document(document_id = value)
                                elif isinstance(value, Document) == False:
                                    raise ValueError(
                                        _(__name__ +
                                          ".exceptions.user_field_does_not_understand_anything_but_Document_objects"
                                          ))
                                field.text = str(value.id)
                            return
                        elif datatype == FieldDataType.CLIENT:
                            if value != False:
                                if isinstance(value, str):
                                    value = Client.find_one(uuid.UUID(value))
                                elif isinstance(value, uuid.UUID):
                                    value = Client.find_one(value)
                                elif isinstance(value, Client) == False:
                                    raise ValueError(
                                        _(__name__ +
                                          ".exceptions.client_field_does_not_understand_anything_but_Client_objects"
                                          ))
                                field.text = str(value.id)
                            return
                        else:
                            raise DocumentFieldNotFound(
                                _(__name__ +
                                  ".exceptions.document_field_type_not_found ")
                                + key)
        raise DocumentFieldNotFound(
            _(__name__ + ".exceptions.document_field_not_found" + key))

    def set_fields(self, fields):
        for key, value in fields.items():
            if key[-12:] != "_inner_value":
                self.set_field_value(key, value)

    def get_field_dict(self):
        fields = {}
        for page in self.document_xml.iterfind('structuredData/page'):
            for line in page.iterfind('line'):
                for field in line.iterfind('field'):
                    if (field.get('id') is not None
                            and field.get('dataType') is not None
                            and field.get('type') is not None
                            and field.get('type').lower() != 'label'):
                        data_type = FieldDataType.to_enum(
                            field.get('dataType'))
                        if (data_type == FieldDataType.DATE):
                            if field.text is not None:
                                fields[field.attrib['id']] = dateparser.parse(
                                    field.text)
                            else:
                                fields[field.attrib['id']] = None

                        elif (data_type == FieldDataType.UUID):
                            if field.text is not None:
                                fields[field.attrib['id']] = uuid.UUID(
                                    field.text)
                            else:
                                fields[field.attrib['id']] = None
                        elif (data_type == FieldDataType.CLIENT):
                            if field.text is not None:
                                client = Client.find_one(uuid.UUID(
                                    field.text))
                                fields[field.attrib['id']] = client
                            else:
                                fields[field.attrib['id']] = None
                        elif (data_type == FieldDataType.USER):
                            if field.text is not None:
                                user = User.find_one(uuid.UUID(
                                    field.text))
                                fields[field.attrib['id']] = user
                            else:
                                fields[field.attrib['id']] = None
                        elif (data_type == FieldDataType.DOCUMENT):
                            if field.text is not None:
                                document = Document(document_id=field.text)
                                fields[field.attrib['id']] = document
                            else:
                                fields[field.attrib['id']] = None
                        elif (data_type == FieldDataType.FLOAT):
                            if field.text is not None:
                                fields[field.attrib['id']] = float(field.text)
                            else:
                                fields[field.attrib['id']] = None
                        elif (data_type == FieldDataType.INTEGER):
                            if field.text is not None:
                                fields[field.attrib['id']] = int(
                                    float(field.text))
                            else:
                                fields[field.attrib['id']] = None
                        elif (data_type == FieldDataType.BOOLEAN):
                            if field.text is not None:
                                if (field.text.lower() == 'yes'
                                        or field.text.lower() == 'true'):
                                    fields[field.attrib['id']] = True
                                elif (field.text.lower() == 'no'
                                      or field.text.lower() == 'false'):
                                    fields[field.attrib['id']] = True
                            else:
                                fields[field.attrib['id']] = None
                        else:
                            fields[field.attrib['id']] = field.text
        return fields

    def get_header_field_dict(self, shallow=False):
        """
        Returns a dictionary with all the header fields. If shallow is set to True, then only the IDs
        of the referenced documents are returned
        """
        fields = {}
        fields['document_id'] = self.get_header_field('document_id', shallow)
        fields['base_document'] = self.get_header_field(
            'base_document', shallow)
        fields['period'] = self.get_header_field('period', shallow)
        fields['concept_type'] = self.get_header_field('concept_type', shallow)
        fields['branch'] = self.get_header_field('branch', shallow)
        fields['client'] = self.get_header_field('client', shallow)
        fields['account_type'] = self.get_header_field('account_type', shallow)
        fields['active_version'] = self.get_header_field(
            'active_version', shallow)
        fields['associated_to'] = self.get_header_field(
            'associated_to', shallow)
        fields['association_type'] = self.get_header_field(
            'association_type', shallow)
        fields['creation_date'] = self.get_header_field(
            'creation_date', shallow)

        fields['draft_date'] = self.get_header_field('draft_date', shallow)
        fields['delete_case'] = self.get_header_field('delete_case', shallow)
        fields['related_case'] = self.get_header_field('related_case', shallow)
        fields['status'] = self.get_header_field('status', shallow)
        fields['document_version'] = self.get_header_field(
            'document_version', shallow)
        fields['hash'] = self.get_header_field('hash', shallow)
        fields['origin'] = self.get_header_field('origin', shallow)
        fields['save_date'] = self.get_header_field('save_date', shallow)
        fields['author'] = self.get_header_field('author', shallow)
        fields['hrn_code'] = self.get_header_field('hrn_code', shallow)
        fields['hrn_title'] = self.get_header_field('hrn_title', shallow)
        fields['secondary_client'] = self.get_header_field(
            'secondary_client', shallow)

        return fields

    def get_header_field(self, key, shallow=False):
        """
        Returns the value of the requested header field. If shallow is set to True, then only the IDs
        of the referenced documents are returned
        """
        headerElements = self.document_xml.find('headerElements')
        accountingElements = headerElements.find('accountingElements')

        if (key.lower() == 'base_document'):
            base_document_node = accountingElements.find('baseDocument')
            if (base_document_node is not None and base_document_node):
                try:
                    base_document_id = uuid.UUID(base_document_node.text)
                    if (shallow is False):
                        document = Document(base_document_id)
                        if (document is not None):
                            return document
                        else:
                            return None
                    else:
                        return base_document_id
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'period'):
            period_node = accountingElements.find('period')
            if (period_node is not None and period_node.text):
                try:
                    return int(float(period_node.text))
                except Exception:
                    return None
            else:
                return None
        elif (key.lower() == 'concept_type'):
            concept_type_node = accountingElements.find('conceptType')
            if (concept_type_node is not None and concept_type_node.text):
                try:
                    concept_type_id = uuid.UUID(concept_type_node.text)
                    if (shallow == False):
                        concept_type = ConceptType.find_one(concept_type_id)
                        if (concept_type is not None):
                            return concept_type
                        else:
                            return None
                    else:
                        return concept_type_id
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'client'):
            client_node = accountingElements.find('client')
            if (client_node is not None and client_node.text):
                try:
                    client_id = uuid.UUID(client_node.text)
                    if (shallow == False):
                        client = Client.find_one(client_id)
                        if (client is not None):
                            return client
                        else:
                            return None
                    else:
                        return client_id
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'branch'):
            branch_node = accountingElements.find('branch')
            if (branch_node is not None and branch_node.text):
                try:
                    branch_id = uuid.UUID(branch_node.text)
                    if (shallow == False):
                        branch = ClientBranch.find_one(branch_id)
                        if (branch is not None):
                            return branch
                        else:
                            return None
                    else:
                        return client_id
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'account_type'):
            account_type_node = accountingElements.find('accountType')
            if (account_type_node is not None and account_type_node.text):
                try:
                    account_type_id = uuid.UUID(account_type_node.text)
                    if (shallow == False):
                        account_type = AccountType.find_one(account_type_id)
                        if (account_type is not None):
                            return account_type
                        else:
                            return None
                    else:
                        return uuid.UUID(account_type_id)
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'active_version'):
            active_version_node = headerElements.find('activeVersion')
            if (active_version_node is not None and active_version_node.text
                    and (active_version_node.text.lower() == 'yes'
                         or active_version_node.text.lower() == 'true')):
                return True
            else:
                return False

        elif (key.lower() == 'associated_to'):
            associated_to_node = headerElements.find('associatedTo')
            if (associated_to_node is not None and associated_to_node.text):
                try:
                    associated_to_uuid = uuid.UUID(associated_to_node.text)
                    if (shallow is False):
                        document = Document(associated_to_uuid)
                        if (document is not None):
                            return document
                        else:
                            return None
                    else:
                        return associated_to_uuid
                except ValueError:
                    return None
            else:
                return None

        elif (key.lower() == 'association_type'):
            association_type_node = headerElements.find('associationType')
            if (association_type_node is not None
                    and association_type_node.text):
                return DocumentAssociationType.to_enum(
                    association_type_node.text)
            else:
                return None

        elif (key.lower() == 'creation_date'):
            creation_date_node = headerElements.find('creationDate')
            if (creation_date_node is not None and creation_date_node.text):
                try:
                    return dateparser.parse(creation_date_node.text)
                except ValueError:
                    return None
            else:
                return None

        elif (key.lower() == 'draft_date'):
            draft_date_node = headerElements.find('draftDate')
            if (draft_date_node is not None and draft_date_node.text):
                try:
                    return dateparser.parse(draft_date_node.text)
                except ValueError:
                    return None
            else:
                return None

        elif (key.lower() == 'delete_case'):
            delete_case_node = headerElements.find('deleteCase')
            if (delete_case_node is not None and delete_case_node.text):
                try:
                    delete_case_uuid = uuid.UUID(delete_case_node.text)
                    if (shallow == False):
                        delete_case = FlowCase.find_one(delete_case_uuid)
                        if (delete_case is not None):
                            return delete_case
                        else:
                            return None
                    else:
                        return delete_case_uuid
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'related_case'):
            related_case_node = headerElements.find('relatedCase')
            if (related_case_node is not None and related_case_node.text):
                try:
                    related_case_uuid = uuid.UUID(related_case_node.text)
                    if (shallow == False):
                        flow_case = FlowCase.find_one(related_case_uuid)
                        if (flow_case is not None):
                            return flow_case
                        else:
                            return None
                    else:
                        return uuid.UUID(related_case_uuid)
                except ValueError:
                    return None
            else:
                return None

        elif (key.lower() == 'status'):
            status_node = headerElements.find('status')
            if (status_node is not None and status_node.text):
                return DocumentStatusType.to_enum(status_node.text)
            else:
                return None
        elif (key.lower() == 'document_version'):
            document_version_node = headerElements.find('documentVersion')
            if (document_version_node is not None
                    and document_version_node.text):
                try:
                    return int(float(document_version_node.text))
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'document_id'):
            document_id = self.document_xml.get('documentId')
            if (document_id is not None):
                try:
                    return uuid.UUID(document_id)
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'hash'):
            hash_node = headerElements.find('hash')
            if (hash_node is not None and hash_node.text):
                return hash_node.text
            else:
                return None

        elif (key.lower() == 'origin'):
            origin_node = headerElements.find('origin')
            if (origin_node is not None and origin_node.text):
                return DocumentOriginType.to_enum(origin_node.text)
            else:
                return None

        elif (key.lower() == 'save_date'):
            save_date_node = headerElements.find('saveDate')
            if (save_date_node is not None and save_date_node.text):
                try:
                    return dateparser.parse(save_date_node.text)
                except ValueError:
                    return None
            else:
                return None

        elif (key.lower() == 'author'):
            author_node = headerElements.find('author')
            if (author_node is not None and author_node.text):
                try:
                    author_uuid = uuid.UUID(author_node.text)
                    if (shallow == False):
                        return User.find_one(author_uuid)
                    else:
                        return author_uuid
                except ValueError:
                    return None
            else:
                return None
        elif (key.lower() == 'hrn_code'):
            hrn_string_node = headerElements.find('hrnCode')
            if (hrn_string_node is not None and hrn_string_node.text):
                return hrn_string_node.text
            else:
                return None
        elif (key.lower() == 'hrn_title'):
            hrn_title_node = headerElements.find('hrnTitle')
            if (hrn_title_node is not None and hrn_title_node.text):
                return hrn_title_node.text
            else:
                return None

        elif (key.lower() == 'secondary_client'):
            secondary_client_node = headerElements.find('secondaryClient')
            if (secondary_client_node is not None
                    and secondary_client_node.text):
                try:
                    secondary_client_uuid = uuid.UUID(
                        secondary_client_node.text)
                    if (shallow == False):
                        secondary_client = Client.find_one(
                            secondary_client_uuid)
                        if (secondary_client is not None):
                            return secondary_client
                        else:
                            return None
                    else:
                        return uuid.UUID(secondary_client_uuid)
                except ValueError:
                    return None
            else:
                return None

        raise ValueError(
            _('antares.app.document.manager.invalid_header_field'))

    def set_header_field(self, key, value):
        headerElements = self.document_xml.find('headerElements')
        accountingElements = headerElements.find('accountingElements')
        if key.lower() == 'obligation_id':
            #this is an special header field that extracts the account info from the
            # obligation object and populates it to the account.
            if isinstance(value, str):
                obligation = ObligationVector.find_one(uuid.UUID(value))
                if (obligation is None):
                    raise InvalidDocumentValueException(
                        _(__name__ + ".exceptions.invalid_obligation_specified"
                          ))
            elif isinstance(value, uuid.UUID):
                obligation = ObligationVector.find_one(value)
                if (obligation is None):
                    raise InvalidDocumentValueException(
                        _(__name__ + ".exceptions.invalid_obligation_specified"
                          ))
            else:
                obligation = value
            if (obligation.compliance_document is not None):
                raise InvalidDocumentValueException(
                    _(__name__ +
                      ".exceptions.the_obligation_already_has_a_compliance_document"
                      ))
            if obligation.client:
                self.set_header_field('client', obligation.client)
            if obligation.period:
                self.set_header_field('period', obligation.period)
            if obligation.concept_type:
                self.set_header_field('concept_type', obligation.concept_type)
            if obligation.account_type:
                self.set_header_field('account_type', obligation.account_type)
            if obligation.base_document:
                self.set_header_field('account_document',
                                      obligation.base_document)
            obligation.compliance_document = self.header
            obligation.save()
        elif key.lower() == 'activity_id':
            #another special one, this one to set the related case
            if isinstance(value, str):
                activity = FlowActivity.find_one(uuid.UUID(value))
                if (activity is None):
                    raise InvalidDocumentValueException(
                        _(__name__ + ".exceptions.invalid_activity_specified"))
            elif isinstance(value, uuid.UUID):
                activity = FlowActivity.find_one(value)
                if (activity is None):
                    raise InvalidDocumentValueException(
                        _(__name__ + ".exceptions.invalid_obligation_specified"
                          ))
            else:
                activity = value
            self.set_header_field('flow_case', activity.flow_case)
        elif key.lower() == 'account_document':
            base_document_node = accountingElements.find('baseDocument')
            if (isinstance(value, Document)):
                base_document_node.text = str(value.document_id)
            elif (isinstance(value, uuid.UUID)):
                base_document_node.text = str(value)
            elif (isinstance(value, str)):
                try:
                    base_document_node.text = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _(__name__ +
                      ".exceptions.invalid_account_document_specified"))
        elif (key.lower() == 'period'):
            period_node = accountingElements.find('period')
            period_node.text = str(value)
        elif (key.lower() == 'concept_type'):
            concept_type_node = accountingElements.find('conceptType')
            if (isinstance(value, ConceptType)):
                concept_type_node.text = str(value.id)
            elif (isinstance(value, uuid.UUID)):
                concept_type_node.text = str(value)
            elif (isinstance(value, str)):
                try:
                    concept_type_node.text = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _(__name__ + ".exceptions.invalid_concept_type_specified"))

        elif (key.lower() == 'client'):
            client_node = accountingElements.find('client')
            if (isinstance(value, Client)):
                client_node.text = str(value.id)
            elif (isinstance(value, uuid.UUID)):
                client_node.text = str(value)
            elif (isinstance(value, str)):
                try:
                    client_node.text = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _(__name__ + ".exceptions.invalid_client_specified"))
        elif (key.lower() == 'branch'):
            client_branch_node = accountingElements.find('branch')
            if (isinstance(value, ClientBranch)):
                client_branch_node.text = str(value.id)
            elif (isinstance(value, uuid.UUID)):
                client_branch_node.text = str(value)
            elif (isinstance(value, str)):
                try:
                    client_branch_node.text = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _(__name__ + ".exceptions.invalid_client_specified"))

        elif (key.lower() == 'account_type'):
            account_type_node = accountingElements.find('accountType')
            if (isinstance(value, AccountType)):
                account_type_node.text = str(value.id)
            elif (isinstance(value, uuid.UUID)):
                account_type_node.text = str(value)
            elif (isinstance(value, str)):
                try:
                    account_type_node.text = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _(__name__ + ".exceptions.invalid_account_type_specified"))

        elif (key.lower() == 'active_version'):
            active_version_node = headerElements.find('activeVersion')
            if (isinstance(value, bool)):
                if (active_version_node == True):
                    active_version_node.text = 'true'
                else:
                    active_version_node.text = 'false'
                headerElements.activeVersion = value
            elif (isinstance(value, str)):
                if (value.lower() == "yes" or value.lower() == "true"):
                    active_version_node.text = 'true'
                if (value.lower() == "no" or value.lower() == "false"):
                    active_version_node.text = 'false'
            else:
                raise InvalidDocumentValueException(
                    _(__name__ + ".exceptions.invalid_active_version_option"))

        elif (key.lower() == 'associated_to'):
            associated_to_node = headerElements.find('associatedTo')
            if (isinstance(value, Document)):
                associated_to_node.text = value.document_id
            elif (isinstance(value, uuid.UUID)):
                associated_to_node.text = str(value)
            elif (isinstance(value, str)):
                try:
                    associated_to_node.text = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _(__name__ +
                      ".exceptions.invalid_account_document_specified"))

        elif (key.lower() == 'association_type'):
            association_type_node = headerElements.find('associationType')
            if (isinstance(value, DocumentAssociationType)):
                association_type_node.text = str(value)
            else:
                association_type_node.text = value
        elif (key.lower() == 'form_version'):
            form_version_node = headerElements.find('formVersion')
            form_version_node.text = value
        elif (key.lower() == 'form_name'):
            form_name_node = headerElements.find('formName')
            form_name_node.text = value
        elif (key.lower() == 'creation_date'):
            creation_date_node = headerElements.find('creationDate')
            creation_date_node.text = value.isoformat()

        elif (key.lower() == 'draft_date'):
            draft_date_node = headerElements.find('draftDate')
            if (isinstance(value, datetime)):
                draft_date_node.text = value.isoformat()
            else:
                draft_date_node.text = value
        elif (key.lower() == 'delete_case'):
            delete_case_node = headerElements.find('deleteCase')
            if (isinstance(value, FlowCase)):
                delete_case_node.text = str(value.id)
            elif (isinstance(value, uuid.UUID)):
                delete_case_node.text = str(value)
            elif (isinstance(value, str)):
                try:
                    delete_case_node.text = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _(__name__ + ".exceptions.invalid_delete_case_specified"))

        elif (key.lower() == 'flow_case'):
            flow_case_node = headerElements.find('flowCase')
            if (isinstance(value, FlowCase)):
                flow_case_node.text = str(value.id)
            elif (isinstance(value, uuid.UUID)):
                flow_case_node.text = str(value)
            elif (isinstance(value, str)):
                try:
                    flow_case_node.text = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _(__name__ + ".exceptions.invalid_flow_case_specified"))

            # We have to link it with the flow case
            pass
        elif (key.lower() == 'status'):
            status_node = headerElements.find('status')
            if (isinstance(value, DocumentStatusType)):
                status_node.text = str(value)
            else:
                status_node.text = value
        elif (key.lower() == 'document_version'):
            document_version_node = headerElements.find('documentVersion')
            document_version_node.text = str(value)
        elif (key.lower() == 'hash'):
            hash_node = headerElements.find('hash')
            hash_node.text = value
        elif (key.lower() == 'origin'):
            origin_node = headerElements.find('origin')
            if (isinstance(value, DocumentOriginType)):
                origin_node.text = str(value)
            else:
                origin_node.text = value
        elif (key.lower() == 'save_date'):
            save_date_node = headerElements.find('saveDate')
            if (isinstance(value, datetime)):
                save_date_node.text = value.isoformat()
            else:
                save_date_node.text = value
        elif (key.lower() == 'author'):
            author_node = headerElements.find('author')
            author_name_node = headerElements.find('authorName')
            if (isinstance(value, User)):
                author_node.text = str(value.id)
                author_name_node.text = value.username
            elif (isinstance(value, uuid.UUID)):
                author = User.find_one(value)
                if (author is not None):
                    author_node.text = str(author.id)
                    author_name_node.text = author.full_name
            else:
                try:
                    author = User.find_one(uuid.UUID(value))
                    if (author is not None):
                        author_node.text = str(author.id)
                        author_name_node.text = author.full_name
                except:
                    # we don't put up with garbage
                    pass

        elif (key.lower() == 'hrn_code'):
            hrn_code_node = headerElements.find('hrnCode')
            if (hrn_code_node is not None):
                hrn_code_node.text = str(value)

        elif (key.lower() == 'hrn_title'):
            hrn_title_node = headerElements.find('hrnTitle')
            if (hrn_title_node is not None):
                hrn_title_node.text = str(value)

        elif (key.lower() == 'secondary_client'):
            secondary_client_node = headerElements.find('secondaryClient')
            if (isinstance(value, Client)):
                secondary_client_node = str(value.id)
            elif (isinstance(value, uuid.UUID)):
                secondary_client_node = str(value)
            elif (isinstance(value, str)):
                try:
                    secondary_client_node = str(uuid.UUID(value))
                except:
                    pass
            else:
                raise InvalidDocumentValueException(
                    _("antares.app.document.manager.invalid_client_specified"))

        else:
            raise ValueError(
                _('antares.app.document.manager.invalid_header_field %(key)s')
                % {
                    'key': key
                })

    def set_header_fields(self, fields):
        for key, value in fields.items():
            self.set_header_field(key, value)

    def set_status(self, status_type):
        if isinstance(status_type, str):
            status = DocumentStatusType.to_enum(status_type)
        else:
            status = status_type

        if status is None:
            raise InvalidDocumentStatusException(
                _(__name__ + ".exceptions.invalid_document_status"))
        prev_status = self.header.status
        if ((status == DocumentStatusType.CANCELLED
             or status == DocumentStatusType.DELETED) and not prev_status):
            raise InvalidDocumentStatusException(
                _(__name__ +
                  ".exceptions.cannot_change_status_if_cancelled_exception"))
        if (status == DocumentStatusType.SAVED
                and prev_status is not DocumentStatusType.DRAFTED):
            raise InvalidDocumentStatusException(
                _("antares.apps.document.type.invalid_status_progression"))
        if (status == DocumentStatusType.SAVED and self.get_author() is None):
            raise InvalidDocumentStatusException(
                _(__name__ + ".exceptions.cannot_save_without_author"))
        if (status == DocumentStatusType.SAVED):
            self.set_header_field('save_date', timezone.now())
        elif (status == DocumentStatusType.DRAFTED):
            self.set_header_field('draft_date', timezone.now())
        elif (status == DocumentStatusType.DELETED):
            self.set_header_field('delete_date', timezone.now())
        self.set_header_field('status', status)

    def get_status(self):
        status_value = self.get_header_field('status', True)
        if (status_value is None):
            return DocumentStatusType.DRAFTED
        else:
            return status_value

    def set_document_version(self, value):
        self.set_header_field("document_version", value)

    def get_document_version(self):
        return self.get_header_field('document_version')

    def get_document_id(self):
        return self.document_id

    def set_active_version(self, value):
        self.set_header_field('active_version', value)

    def is_active_version(self):
        return self.get_header_field('active_version')

    def set_author(self, value):
        self.set_header_field('author', value)

    def get_author(self, shallow=False):
        return self.get_header_field('author', shallow)

    def get_save_date(self):
        return self.get_header_field('save_date')

    def set_save_date(self, date):
        return self.set_header_field('save_date', date)

    def get_form_definition(self):
        return self.header.form_definition

    def get_draft_date(self):
        return self.get_header_field('draft_date')

    def set_draft_date(self, date):
        return self.set_header_field('draft_date', date)

    def get_creation_date(self):
        return self.get_header_field('creation_date')

    def set_creation_date(self, date):
        return self.set_header_field('creation_date', date)

    def get_delete_date(self):
        return self.get_header_field('delete_date')

    def set_delete_case(self, value):
        self.set_header_field('delete_case', value)

    def get_delete_case(self, shallow=False):
        return self.get_header_field('delete_case', shallow)

    def get_delete_comment(self):
        return self.get_header_field('delete_comment')

    def set_association_information(self, association_type, associated_to):
        if (association_type is not None and associated_to is not None):
            self.set_header_field('association_type', association_type)
            self.set_header_field('associated_to', associated_to)

    def get_origin(self):
        return self.get_header_field('origin')

    def set_origin(self, value):
        self.set_header_field('origin', value)

    def get_hrn_script(self):
        return self.get_header_field('hrn_script')

    def set_hrn_script(self, value):
        self.set_header_field('hrn_script', value)

    def get_hrn_title(self):
        return self.get_header_field('hrn_title')

    def set_hrn_title(self, value):
        self.set_header_field('hrn_title', value)

    def get_hash(self):
        return self.get_header_field('hash')

    def set_hash(self, value):
        self.set_header_field('hash', value)

    def set_period(self, value):
        self.set_header_field('period', value)

    def set_concept_type(self, value):
        self.set_header_field('concept_type', value)

    def set_secondary_client(self, value):
        self.set_header_field('secondary_client', value)

    def set_account_type(self, value):
        self.set_header_field('account_type', value)

    def set_client(self, value):
        self.set_header_field('client', value)

    def save(self, status_type=None):
        from antares.apps.accounting.manager import AccountManager
        from antares.apps.notifications.manager import NotificationManager
        from antares.apps.subscription.manager import SubscriptionManager

        if (isinstance(status_type, str)):
            status_type = DocumentStatusType.to_enum(status_type)

        self._evaluate_field_calculation()
        self._validate_fields()
        self._check_required_fields()
        self._hibernate_document()

        if (status_type is not None):
            self.set_status(status_type)

        if (status_type == DocumentStatusType.SAVED):
            #field validation
            self._validate_fields()
            self._check_required_fields()
            self._process_modules_hooks()
            self.header.hash = self.hash()
            self.header.save()
            AccountManager.post_document(self)
            SubscriptionManager.process_document_subscriptions(self)
            NotificationManager.post_document(self)
            
    def hash(self):
        doc_xml = etree.fromstring(etree.tostring(self.document_xml))
        headerElements = doc_xml.find('headerElements')

        #we need to exclude hash as it produces different results
        doc_hash = headerElements.find('hash')
        if (doc_hash is not None):
            doc_hash.text = None

        digest = hashlib.sha256(
            etree.tostring(self.document_xml, pretty_print=True))
        self.set_hash(digest.hexdigest())
        return digest.hexdigest()

    def verify_hash_digest(self):
        """verifies the hash with the hydrated XML """
        doc_hash = self.hash()

        logger.info("calculated hash is " + doc_hash + " and stored hash is " +
                    self.header.hash)
        if self.header.hash == doc_hash:
            return True
        else:
            return False

    def _evaluate_field_calculation(self):
        fields = self.get_field_dict()
        fields['header_fields'] = self.get_header_field_dict(False)
        fields['document'] = self
        fields['logger'] = logger

        calculated_nodes = self.document_xml.find(
            'structuredData/page/line/field[@calculate]')
        if calculated_nodes is None:
            #nothing to calculate
            return

        calculated_nodes[:] = sorted(
            calculated_nodes, key=self.__get_calculated_node_key)
        for calculated_node in self.document_xml.iterfind(
                'structuredData/page/line/field[@calculate]'):
            #we need to declare the context each time to allow for nested calculations
            context = js2py.EvalJs(fields)
            context.execute(
                calculated_node.get('id') + ' = ' +
                calculated_node.get('calculate'))
            fields[calculated_node.get('id')] = eval(
                'context.' + calculated_node.get('id'))
            self.set_field_value(
                calculated_node.get('id'), fields[calculated_node.get('id')])
            logger.debug(
                _(__name__ +
                  ".new_value_for_calculated_field {field_id} {calculation_result} {calculation_order}"
                  ).format(
                      field_id=calculated_node.get('id'),
                      calculation_order=calculated_node.get(
                          'calculationOrder'),
                      calculation_result=fields[calculated_node.get('id')]))

    def _validate_fields(self):
        logger.info(_(__name__ + ".validation_started"))
        fields = self.get_field_dict()
        fields['header_fields'] = self.get_header_field_dict(False)
        fields['document'] = self
        fields['logger'] = logger

        context = js2py.EvalJs(fields)

        for validation_node in self.document_xml.iterfind(
                'structuredData/page/line/field[@validate]'):
            #we need to declare the context each time to allow for nested calculations
            context.execute(
                'return_value = ' + validation_node.get('validate'))
            logger.debug(
                _(__name__ +
                  ".validation_result {field_id} {validation_result} {validation}"
                  ).format(
                      field_id=validation_node.get('id'),
                      validation_result=context.return_value),
                validation=validation_node.get('id'))

            if (hasattr(context, 'return_value')
                    and context.return_value != True):
                raise DocumentValidationException(
                    validation_node.get('validationMessage'))

    def _check_required_fields(self):
        logger.info(_(__name__ + ".required_fields_start"))
        fields = self.get_field_dict()
        for required_node in self.document_xml.iterfind(
                'structuredData/page/line/field[@required="yes"]'):
            if (required_node.get('id') in fields
                    and (fields[required_node.get('id')] is None
                         or len(fields[required_node.get('id')]) == 0)):
                raise DocumentRequiredException(
                    required_node.get('requiredMessage'))

    def __get_calculated_node_key(self, node):
        """
        
        """
        try:
            return int(float(node.get('calculationOrder')))
        except ValueError:
            return 0

    def __get_source_definition(self, node):
        """
        
        """
        try:
            return node.get('source')
        except ValueError:
            return None

    def get_client(self):
        return self.get_header_field('client')

    def set_account_information(self, client, concept_type, period,
                                account_type, base_document):
        """
        A simple method to add the information related to the accounting side in
        an easy manner.
        """
        if (client is not None and isinstance(client, Client)):
            self.set_header_field('client', client)
        if (concept_type is not None
                and isinstance(concept_type, ConceptType)):
            self.set_header_field('concept_type', concept_type)
        if (period is not None and isinstance(period, int)):
            self.set_header_field('period', period)
        if (account_type is not None
                and isinstance(account_type, AccountType)):
            self.set_header_field('account_type', account_type)
        if (base_document is not None and isinstance(base_document, Document)):
            self.set_header_field('account_type', base_document.header)

    def _map_header_fields_to_fields(self):
        """ This simply maps the header fields into the body
        """
        for field in self.document_xml.iterfind(
                'structuredData/page/line/field[@headerField]'):
            header_field_id = field.get("headerField")
            if (header_field_id):
                header_value = self.get_header_field(header_field_id, True)
                if (header_value):
                    field.text = str(header_value)

    def _map_fields_to_header_fields(self):
        """ This simply maps the fields into the header
        """
        for field in self.document_xml.iterfind(
                'structuredData/page/line/field[@headerField]'):
            header_field_id = field.get("headerField")
            if (header_field_id):
                header_value = self.get_header_field(header_field_id, True)
                if (header_value):
                    header_value = field.text

    def _process_hrn_script(self, event_type):

        HrnCode.process_document_hrn_script(self, event_type)

    def _process_functions(self, event_type):
        for external_function_node in self.document_xml.iterfind(
                'headerElements/externalFunctions/externalFunction'):
            events = self._process_external_function_events(
                external_function_node)
            if (event_type in events):
                for external_function_code_node in external_function_node.iterfind(
                        'code'):
                    language = ScriptEngineType.to_enum(
                        external_function_code_node.get('language'))
                    code = external_function_code_node.text
                    if (code and language):
                        self._process_inline_function(event_type, code,
                                                      language)
                    else:
                        raise NotImplementedError

    def _process_inline_function(self, event_type, code, language):
        fields = self.get_field_dict()
        header_fields = self.get_header_field_dict(False)
        if (language == ScriptEngineType.PYTHON):
            # remember to access the document directly
            eval(code)
        elif (language == ScriptEngineType.JAVASCRIPT):
            fields['user'] = get_request().user
            fields['event_type'] = event_type
            fields['header_fields'] = header_fields
            fields['document'] = self
            fields['logger'] = logger
            context = js2py.EvalJs(fields)
            # here access the document directly
            context.execute(code)
        else:
            raise NotImplementedError

    def _process_external_function_events(self, event):
        events = []
        for external_function_node in self.document_xml.iterfind(
                'headerElements/externalFunctions/externalFunction'):
            event_text = external_function_node.get('events')
            if (event_text):
                event_list = event_text.split(',')
                for event in event_list:
                    if (DocumentEventType.to_enum(event.strip())):
                        events.append(DocumentEventType.to_enum(event.strip()))

        return events

    def _process_modules_hooks(self):
        from antares.apps.accounting.manager import AccountManager
        from antares.apps.subscription.manager import SubscriptionManager
        from antares.apps.obligation.constants import ObligationStatusType

        SubscriptionManager.process_document_subscriptions(self)
        #if an account rule is set for the form_def we post it to the accounting system
        account_rule_count = self.header.form_definition.account_rule_set.select_related(
        ).count()
        if (account_rule_count > 1):
            AccountManager.post_document(self)

        #this is to set all obligations set as compliant
        for obligation in self.header.obligation_vector_compliance_document_set.select_related(
        ).all():
            obligation.status = ObligationStatusType.COMPLIANT
            obligation.compliance_date = self.get_save_date()
            obligation.save()

    def _process_field_sources(self):
        """ Gathers information from the system and plugs it to the fields
        
        """
        #we only do this if the document is in DRAFTED status.
        if self.get_status() != DocumentStatusType.DRAFTED:
            return None
        fields = {}
        fields['client'] = get_request().user.get_on_behalf_client()
        fields['user'] = get_request().user
        fields['sysdate'] = datetime.now()
        context = js2py.EvalJs(fields)
        for field_node in self.document_xml.xpath(
                "//field[@type!='label' and @source]"):
            context.execute("result = " + field_node.get('source'))
            result = context['result']
            if result is not None:
                self.set_field_value(field_node.get('id'), result)
