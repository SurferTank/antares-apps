'''
Created on Nov 5, 2017

@author: leobelen
'''
import logging
import json
from django.utils.translation import ugettext as _
from antares.apps.document.models import FormDefinition
from antares.apps.document.types import Document
from antares.apps.document.constants import DocumentStatusType
from antares.apps.core.middleware import get_request
from typing import List

logger = logging.getLogger(__name__)


class MessageManager:
    @classmethod
    def create_docs_from_message(cls, msg_json: str) -> List[Document]:
        """ create documents from the message passed
        :param msg_json: the message to process
        """
        document_list = list()
        msg = json.loads(msg_json)
        for msgdoc in msg['documents']:
            logger.debug(msgdoc['type'])
            form_def = FormDefinition.find_one_by_third_party_type(
                msgdoc['type'])
            if form_def is None:
                raise ValueError(
                    _(__name__ +
                      ".exceptions.third_party_form_does_not_exist"))
            document = Document(form_id=form_def.id)
            if document is None:
                raise ValueError(
                    _(__name__ + ".exceptions.document_could_not_be_created"))
            #lets push all header fields
            for header_field in msgdoc['header']:
                for key, value in header_field.items():
                    document.set_header_field(key, value)
            for field in msgdoc['fields']:
                for key, value in field.items():
                    document.set_field_value(
                        document.get_field_id_by_messagemap(key), value)

            document.set_author(get_request().user)
            document.save(DocumentStatusType.SAVED)
            document_list.append(document)
        return document_list
