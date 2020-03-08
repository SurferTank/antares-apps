from datetime import datetime
import logging
import os

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext as _
from lxml import etree
from lxml import objectify

from antares.apps.core.constants import FieldDataType
from antares.apps.core.manager import PeriodManager
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models.system_parameter import SystemParameter
from antares.apps.document.constants import FormDefinitionStatusType

from ..exceptions import InvalidFormDefinitionException


logger = logging.getLogger(__name__)


class FormDefinition(models.Model):
    id = models.CharField(primary_key=True, max_length=255, editable=False)
    form_class = models.ForeignKey(
        "FormClass",
        on_delete=models.PROTECT,
        db_column='form_class',
        related_name='form_definition_set')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False,
        related_name='form_definition_author_set')
    definition = models.TextField(blank=True)
    description = models.TextField(blank=True, null=True)
    edit_js_xslt = models.TextField(blank=True, null=True)
    edit_xslt = models.TextField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    form_name = models.CharField(max_length=100, editable=False)
    form_version = models.IntegerField(default=0, editable=False)
    hrn_script = models.TextField(blank=True, null=True)
    print_xslt = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    status = models.CharField(choices=FormDefinitionStatusType.choices,
        max_length=30,
        default=FormDefinitionStatusType.DEVELOPMENT)
    view_xslt = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(FormDefinition, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    DOC_DEFAULT_TEMPLATE_MEDIA_ROOT = os.path.join('document', 'templates')

    DOC_DEFAULT_TEMPLATE_OS_HOME = os.path.join('document', 'templates')
    DOC_SCHEMA_LOCATION = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'xml',
        'document_1_0.xsd')
    DOC_XSLT_DEFAULT_EDIT_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'xml',
        'default_document_edit.xslt')
    DOC_XSLT_DEFAULT_EDIT_JS_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'xml',
        'default_document_edit_js.xslt')
    DOC_XSLT_DEFAULT_VIEW_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'xml',
        'default_document_view.xslt')
    DOC_XSLT_DEFAULT_PRINT_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', 'xml',
        'default_document_print.xslt')
    DOC_EDIT_FILE_NAME = "edit.html"
    DOC_EDIT_JS_FILE_NAME = "edit.js"
    DOC_VIEW_FILE_NAME = "view.html"
    DOC_PRINT_FILE_NAME = "print.po"

    def process_form_definition_loading(self):
        separator = SystemParameter.find_one("DEFAULT_FORM_NAME_SEPARATOR",
                                             FieldDataType.STRING, '-')
        definition_obj = etree.fromstring(self.definition)
        self.verify_xml_against_schema()
        form_name = definition_obj.find('headerElements/formName')
        form_version = definition_obj.find('headerElements/formVersion')
        if (form_name is not None and form_name.text
                and form_version is not None and form_version.text):
            self.form_name = form_name.text
            self.form_version = form_version.text
            self.id = "{form_name}{separator}{form_version}".format(
                form_name=self.form_name,
                separator=separator,
                form_version=self.form_version)
        else:
            raise InvalidFormDefinitionException(
                _(__name__ + ".incomplete_form_id_definition"))

        definition_obj = FormDefinition.set_blank_header_xml(definition_obj)
        self.definition = etree.tostring(definition_obj, encoding='unicode', xml_declaration=False)
        self.verify_and_create_supporting_files(True)
        return self

    def verify_xml_against_schema(self):
        path = os.path.isfile(self.DOC_SCHEMA_LOCATION)
        if not path:
            raise FileNotFoundError(
                _(__name__ + ".exceptions.schema_not_found"))

        schema_root = etree.parse(self.DOC_SCHEMA_LOCATION)
        schema = etree.XMLSchema(schema_root)

        parser = etree.XMLParser(schema=schema)
        #try:
        #    etree.fromstring(self.definition, parser)
        #except Exception as e:
        #    raise InvalidFormDefinitionException(
        #        _(__name__ + ".exceptions.form_is_invalid"))

    @classmethod
    def set_blank_header_xml(cls, definition_obj):
        headerElements = definition_obj.find('headerElements')
        accountingElements = headerElements.find('accountingElements')

        if accountingElements is not None:
            client = accountingElements.find('client')
            if (client is not None):
                client.text = None
            base_document = accountingElements.find('baseDocument')
            if (base_document is not None):
                base_document.text = None
            concept_type = accountingElements.find('conceptType')
            if (concept_type is not None):
                concept_type.text = None
            period = accountingElements.find('period')
            if (period is not None):
                period.text = None
            account_type = accountingElements.find('accountType')
            if (account_type is not None):
                account_type.text = None

        document_version = headerElements.find('documentVersion')
        if (document_version is not None):
            document_version.text = None

        document_id = headerElements.find('documentId')
        if (document_id is not None):
            document_id.text = None

        author = headerElements.find('author')
        if (author is not None):
            author.text = None

        author_name = headerElements.find('authorName')
        if (author_name is not None):
            author_name.text = None

        save_date = headerElements.find('saveDate')
        if (save_date is not None):
            save_date.text = None

        draft_date = headerElements.find('draftDate')
        if (draft_date is not None):
            draft_date.text = None

        creation_date = headerElements.find('creationDate')
        if (creation_date is not None):
            creation_date.text = None

        delete_date = headerElements.find('deleteDate')
        if (delete_date is not None):
            delete_date.text = None

        delete_case = headerElements.find('deleteCase')
        if (delete_case is not None):
            delete_case.text = None

        delete_comment = headerElements.find('deleteComent')
        if (delete_comment is not None):
            delete_comment.text = None

        associated_to = headerElements.find('associatedTo')
        if (associated_to is not None):
            associated_to.text = None

        association_type = headerElements.find('associationType')
        if (association_type is not None):
            association_type.text = None

        flow_case = headerElements.find('flowCase')
        if (flow_case is not None):
            flow_case.text = None

        origin = headerElements.find('origin')
        if (origin is not None):
            origin.text = None

        status = headerElements.find('status')
        if (status is not None):
            status.text = None

        doc_hash = headerElements.find('hash')
        if (doc_hash is not None):
            doc_hash.text = None

        objectify.deannotate(
            definition_obj, xsi_nil=True, cleanup_namespaces=True)

        return definition_obj

    def verify_and_create_supporting_files(self, creating_forms=False):
        template_home = os.path.join(
            settings.BASE_DIR, settings.BASE_APP_DIR, 'templates',
            self.DOC_DEFAULT_TEMPLATE_OS_HOME, self.id)
        if not os.path.isdir(template_home):
            os.makedirs(template_home)
        template_media_home = os.path.join(
            settings.MEDIA_ROOT, self.DOC_DEFAULT_TEMPLATE_MEDIA_ROOT, self.id,
            'js')
        if not os.path.exists(template_media_home):
            os.makedirs(template_media_home)
        self.verify_xml_against_schema()
        param_creating_form = SystemParameter.find_one(
            "DOC_DEFAULT_SUPPORTING_FILES_CREATION", FieldDataType.BOOLEAN,
            False)
        if creating_forms == False and param_creating_form == True:
            creating_forms = True

        if os.path.isfile(
                os.path.join(
                    template_home,
                    self.DOC_EDIT_FILE_NAME)) and creating_forms == True:
            os.remove(os.path.join(template_home, self.DOC_EDIT_FILE_NAME))

        if not os.path.isfile(
                os.path.join(template_home, self.DOC_EDIT_FILE_NAME)):
            if self.edit_xslt:
                xslt = etree.fromstring(self.edit_xslt)
            elif os.path.isfile(self.DOC_XSLT_DEFAULT_EDIT_FILE):
                xslt = etree.parse(self.DOC_XSLT_DEFAULT_EDIT_FILE)
            else:
                raise FileNotFoundError
            dom = etree.fromstring(self.definition)
            transform = etree.XSLT(xslt)
            newdom = transform(dom)
            contents = str(newdom)
            with open(
                    os.path.join(template_home, self.DOC_EDIT_FILE_NAME),
                    'w',
                    encoding='utf8') as text_file:
                print(contents, file=text_file)

        if (os.path.isfile(
                os.path.join(template_media_home, self.DOC_EDIT_JS_FILE_NAME))
                and creating_forms == True):
            os.remove(
                os.path.join(template_media_home, self.DOC_EDIT_JS_FILE_NAME))

        if not os.path.isfile(
                os.path.join(template_media_home, self.DOC_EDIT_JS_FILE_NAME)):
            if self.edit_js_xslt:
                xslt = etree.fromstring(self.edit_js_xslt)
            elif os.path.isfile(self.DOC_XSLT_DEFAULT_EDIT_JS_FILE):
                xslt = etree.parse(self.DOC_XSLT_DEFAULT_EDIT_JS_FILE)
            else:
                raise FileNotFoundError
            dom = etree.fromstring(self.definition)
            transform = etree.XSLT(xslt)
            newdom = transform(dom)
            contents = str(newdom)
            with open(
                    os.path.join(template_media_home,
                                 self.DOC_EDIT_JS_FILE_NAME),
                    'w',
                    encoding='utf8') as text_file:
                print(contents, file=text_file)

        if os.path.isfile(
                os.path.join(
                    template_home,
                    self.DOC_VIEW_FILE_NAME)) and creating_forms == True:
            os.remove(os.path.join(template_home, self.DOC_VIEW_FILE_NAME))

        if not os.path.isfile(
                os.path.join(template_home, self.DOC_VIEW_FILE_NAME)):
            if self.view_xslt:
                xslt = etree.fromstring(self.view_xslt)
            elif os.path.isfile(self.DOC_XSLT_DEFAULT_VIEW_FILE):
                xslt = etree.parse(self.DOC_XSLT_DEFAULT_VIEW_FILE)
            else:
                raise FileNotFoundError
            dom = etree.fromstring(self.definition)
            transform = etree.XSLT(xslt)
            newdom = transform(dom)
            contents = str(newdom)
            with open(
                    os.path.join(template_home, self.DOC_VIEW_FILE_NAME),
                    'w+',
                    encoding='utf8') as text_file:
                print(contents, file=text_file)
        logger.info('we processed the files for ' + self.id)

    def get_edit_site_path(self):
        return os.path.join(
            SystemParameter.find_one("DOC_DEFAULT_TEMPLATE_OS_HOME",
                                     FieldDataType.STRING,
                                     self.DOC_DEFAULT_TEMPLATE_OS_HOME),
            self.id, self.DOC_EDIT_FILE_NAME)

    def get_edit_js_site_path(self):
        return os.path.join(
            SystemParameter.find_one("DOC_DEFAULT_TEMPLATE_MEDIA_ROOT",
                                     FieldDataType.STRING,
                                     self.DOC_DEFAULT_TEMPLATE_MEDIA_ROOT),
            self.id, 'js', self.DOC_EDIT_JS_FILE_NAME)

    def get_view_site_path(self):
        return os.path.join(
            SystemParameter.find_one("DOC_DEFAULT_TEMPLATE_OS_HOME",
                                     FieldDataType.STRING,
                                     self.DOC_DEFAULT_TEMPLATE_OS_HOME),
            self.id, self.DOC_VIEW_FILE_NAME)

    def get_print_site_path(self):
        return os.path.join(
            SystemParameter.find_one("DOC_DEFAULT_TEMPLATE_OS_HOME",
                                     FieldDataType.STRING,
                                     self.DOC_DEFAULT_TEMPLATE_OS_HOME),
            self.id, self.DOC_PRINT_FILE_NAME)

    @classmethod
    def find_one(cls, form_id):
        try:
            return cls.objects.get(pk=form_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_one_by_concept_type_id_and_period(cls, period, concept_type):
        period_date = PeriodManager.calculate_date_from_period(
            datetime(2001, 1, 1), period)

        try:
            return FormDefinition.objects.filter(
                Q(form_class__concept_type__id=concept_type) &
                Q(start_date__lgt=period_date) & (Q(end_date__gte=period_date)
                                                  | Q(end_date=None)))
        except:
            return None

    @classmethod
    def find_one_by_third_party_type(cls, third_party_type):
        from ..models import FormClass
        try:
            form_class = FormClass.objects.get(
                third_party_type=third_party_type)
            return cls.objects.get(
                Q(form_class=form_class) &
                ~Q(status=FormDefinitionStatusType.DEACTIVATED))
        except:
            return None

    class Meta:
        app_label = 'document'
        db_table = 'doc_form_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
