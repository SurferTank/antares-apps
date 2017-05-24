'''
Created on Jun 21, 2016

@author: leobelen
'''

import logging

from django.utils.translation import ugettext as _

from antares.apps.document.types import Document

from ..manager import NotificationManager

logger = logging.getLogger(__name__)


class NotificationConsole(object):
    @classmethod
    def process_commands(cls, params: list, html: bool=False) -> str:
        message = ""
        if ('post' in params):
            message += cls._post_document(params, html)
        elif ('help' in params):
            message += "We may say that the notification help will show up here"
        else:
            message += _(__package__ + ".messages.dont_now_command")

        return message

    @classmethod
    def _post_document(cls, params: list, html: bool=False) -> str:
        if ('withdocumentid' in params):
            try:
                document = Document(document_id=params['withdocumentid'])
            except Exception:
                return _(__package__ + ".messages.document_error")
        else:
            return _(__package__ +
                     ".messages.missing_parameter {parameter}").format(
                         parameter='withdocumentid')
        NotificationManager.post_document(document)
        return _(
            __package__ +
            ".messages.document_successfully_posted {document_id}").format(
                document_id=document.document_id)
