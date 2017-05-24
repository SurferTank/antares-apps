'''
Created on Jun 21, 2016

@author: leobelen
'''

import logging

from django.utils.translation import ugettext as _

from antares.apps.document.types import Document

from ..manager import AccountManager

logger = logging.getLogger(__name__)


class AccountConsole(object):
    """
        Processes the account console commands
    """

    @classmethod
    def process_commands(cls, params: list, html: bool=False) -> str:
        message = ""
        if 'post' in params:
            message += AccountConsole._post_document(params, html)
        elif 'help' in params:
            message += "We may say that the accounting help will show up here"
        else:
            message += _(__name__ + ".dont_now_command")

        return message

    @classmethod
    def _post_document(cls, params: list, html: bool=False) -> str:
        if 'withdocumentid' in params:
            try:
                document = Document(document_id=params['withdocumentid'])
            except Exception:
                return _(__name__ + ".messages.document_error")
        else:
            return _(__name__ + ".missing_parameter {parameter}").format(
                parameter='withdocumentid')
        AccountManager.post_document(document)
        return _(__name__ +
                 ".document_successfully_posted_to_cca {document_id}").format(
                     document_id=document.document_id)
