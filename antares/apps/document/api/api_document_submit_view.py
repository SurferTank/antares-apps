'''
Created on 16/8/2016

@author: leobelen
'''

import logging

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import View

from antares.apps.core.middleware.request import get_request

from ..enums import DocumentEventType, DocumentStatusType
from ..types import Document

logger = logging.getLogger(__name__)


class ApiDocumentSubmitView(AjaxResponseMixin, JSONResponseMixin, View):
    '''
    classdocs
    '''

    def post(self, request, *args, **kwargs):
        response_dict = {}
        event = DocumentEventType.to_enum(request.POST.get('_event'))
        if (event is None):
            response_dict['errorMessage'] = _(__name__ +
                                              ".exceptions.event_is_missing")
            return self.render_json_response(response_dict)
        fields = {}
        header_fields = {}
        document = None
        for key in request.POST:
            if key.startswith('fields['):
                fields[key.partition('[')[-1].rpartition(']')[
                    0]] = request.POST[key]
            elif key.startswith('headerFields['):
                header_field_name = key.partition('[')[-1].rpartition(']')[0]
                logger.debug('field_name found ' + header_field_name)
                # we exclude the location elements, which cannot be ever
                # changed.
                if (header_field_name not in Document.IMMUTABLE_HEADER_FIELDS):
                    header_fields[header_field_name] = request.POST[key]
                if (header_field_name == 'document_id'):
                    document = Document(document_id=request.POST[key])
                    if (document is None):
                        response_dict['errorMessage'] = _(
                            __name__ + ".exceptions.document_is_missing")
                        return self.render_json_response(response_dict)

        if (document is None):
            response_dict['errorMessage'] = _(
                __name__ + ".exceptions.document_is_missing")
            return self.render_json_response(response_dict)

        if (document.get_status() != DocumentStatusType.DRAFTED):
            response_dict['errorMessage'] = _(
                __name__ +
                ".exceptions.document_is_not_in_draft_mode_and_cannot_be_saved"
            )
            return self.render_json_response(response_dict)

        logger.debug("fields is " + str(fields))
        logger.debug("header_fields is " + str(header_fields))

        document.set_header_fields(header_fields)
        document.set_fields(fields)

        if (event == DocumentEventType.DRAFT_MODIFICATION):
            document.set_author(get_request().user)
            document.set_draft_date(timezone.now())
            document.save(DocumentStatusType.DRAFTED)
        elif (event == DocumentEventType.SAVE):
            document.set_author(get_request().user)
            document.set_save_date(timezone.now())
            document.save(DocumentStatusType.SAVED)

        return self.render_json_response(response_dict)
