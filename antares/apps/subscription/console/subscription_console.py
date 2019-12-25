'''
Created on Jul 15, 2016

@author: leobelen
'''
import logging

from django.utils.translation import ugettext as _

from antares.apps.document.models import DocumentHeader
from antares.apps.document.types import Document

from ..manager import SubscriptionManager


logger = logging.getLogger(__name__)


class SubscriptionConsole(object):
    '''
    classdocs
    '''

    @classmethod
    def process_commands(cls, params, html=False):
        message = ""
        if ('help' in params):
            message += "We may say that the help will show up here"
        elif ('processdocument' in params):
            message += SubscriptionConsole._process_document(params, html)
        else:
            message += _(__name__ + ".dont_now_command")

        return message

    @classmethod
    def _process_document(cls, params, html):
        if ('withdocumentid' in params):
            document = Document(document_id=params['withdocumentid'])
        elif ('withdocumentcode' in params):
            document_header = DocumentHeader.find_one_by_hrn_code(
                params['withdocumentcode'])
            if document_header is None:
                return _(__name__ + ".no_document_found")
            document = Document(document_id=document_header.id)
        else:
            return _(__name__ + ".missing_parameter {parameter}").format(
                parameter='withdocumentid')
        if (document is not None):
            SubscriptionManager.process_document_subscriptions(document)

            return _(
                __name__ +
                ".document_subscription_processed_successfully {document_id}"
            ).format(document_id=document.document_id)
        else:
            return _(__name__ + ".document_not_found")
