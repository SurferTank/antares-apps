""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""

from antares.apps.document.types import Document
import logging
from typing import List

from django.utils.translation import ugettext as _

from ..manager import AccountManager


logger = logging.getLogger(__name__)


class AccountConsole(object):
    """ Processes the account console commands
    """

    @classmethod
    def process_commands(cls, params: List[str], html: bool=False) -> str:
        """ Processes the commands handled off by the terminal module
            
            :param params: the list of parameters to use
            :param html: indicates if the process has to produce output in html format
            :returns: a string with the output
        """
        message = ""
        if 'post' in params:
            message += AccountConsole._post_document(params)
        elif 'help' in params:
            message += "We may say that the accounting help will show up here"
        else:
            message += _(__name__ + ".dont_now_command")

        return message

    @classmethod
    def _post_document(cls, params: List[str]) -> str:
        """ Posts a document to the current account
            
            :param params: the list of parameters to use
            :param html: indicates if the process has to produce output in html format
            :returns: a string with the output
        """
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
