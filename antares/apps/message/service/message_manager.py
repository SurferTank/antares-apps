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
    def process_message(cls, msg: dict) -> List:
        """ 
        Processes a message into Antares
        :param msg_json: the message to process in json format
        """
        result = None
        if msg["action"].lower() == "create":
            result = cls.create_docs_from_message(msg)
        return result

    @classmethod
    def create_docs_from_message(cls, msg: json) -> List[Document]:
        """ 
        Create documents from the message passed
        :param msg: the message to process in json format
        """
        document_list = list()

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
            for key, value in msgdoc['header'].items():
                logger.debug("Header fields => key is " + str(key) +
                             " value is " + str(value))
                document.set_header_field(key, value)
            for key, value in msgdoc['fields'].items():
                logger.debug("Body fields => 3p=" + str(key) + " id=" + (
                    document.get_field_id_by_messagemap(key) or 'None') +
                             " value=" + str(value))
                document.set_field_value(
                    document.get_field_id_by_messagemap(key), value)

            document.set_author(get_request().user)
            document.save(DocumentStatusType.SAVED)
            document_list.append(document)
        return document_list
