'''
Created on 16/8/2016

@author: leobelen
'''

import logging

from django.shortcuts import render
from django.views.generic import View

from antares.apps.core.middleware.request import get_request
from django.conf import settings

from ..constants import FormDefinitionStatusType
from ..models import FormDefinition
from ..types import Document

logger = logging.getLogger(__name__)


class DocumentCreateView(View):
    """
    Handles the interface to create and edit new documents.
    """

    def __init__(self):
        pass

    def get(self, request, form_id):
        header_field_dict = self._get_headers_from_request(request)
        form_definition = FormDefinition.find_one(form_id)
        show_submit = request.GET.get('ss')
        if (show_submit is not None and
            (show_submit.lower() == 'false' or show_submit.lower() == 'f'
             or show_submit.lower() == 'no' or show_submit.lower() == 'n'
             or show_submit.lower() == '0')):
            show_submit = 'false'
        else:
            show_submit = 'true'

        logger.info('show_submit is ' + show_submit)

        if ('is_inner' in request.GET):
            template = 'empty_layout.html'
            is_inner = 'true'
        else:
            template = 'base_layout.html'
            is_inner = 'false'

        if ('next' in request.GET):
            next_place = request.GET.get('next')
        else:
            #TODO: this should be decided first.
            next_place = '/home'

        if (form_definition is None or form_definition.status ==
                FormDefinitionStatusType.DEACTIVATED):
            raise ValueError("Unknown Form ID or the Form is not Active")

        # TODO: Auth is missing here

        document = Document(
            form_id=form_id, header_fields_dict=header_field_dict)

        document.set_author(get_request().user)
        document.save()

        document.get_form_definition().verify_and_create_supporting_files(
            settings.DEBUG)

        edit_js_path = document.get_form_definition().get_edit_js_site_path()
        fields = document.get_field_dict()
        header_fields = document.get_header_field_dict()

        return render(
            request,
            document.get_form_definition().get_edit_site_path(), {
                'document': document.header,
                'headerFields': header_fields,
                'fields': fields,
                'formType': 'CREATION',
                'showSubmit': show_submit,
                'template': template,
                'next_place': next_place,
                'edit_js_path': edit_js_path,
                'is_inner': is_inner,
            })

    def _get_headers_from_request(self, request):
        header_fields_dict = {}
        if (request.GET.get('obligation_id')):
            header_fields_dict['obligation_id'] = request.GET.get(
                'obligation_id')
        if (request.GET.get('activity_id')):
            header_fields_dict['activity_id'] = request.GET.get('activity_id')
        if (request.GET.get('client')):
            if (request.GET.get('client') == 'current'):  # special signal
                header_fields_dict[
                    'client'] = request.user.get_on_behalf_client()
            else:
                header_fields_dict['client'] = request.GET.get(
                    'secondary_client')
        if (request.GET.get('account_type')):
            header_fields_dict['account_type'] = request.GET.get(
                'account_type')
        if (request.GET.get('concept_type')):
            header_fields_dict['concept_type'] = request.GET.get(
                'concept_type')
        if (request.GET.get('period')):
            header_fields_dict['period'] = request.GET.get('period')
        if (request.GET.get('base_document')):
            header_fields_dict['base_document'] = request.GET.get(
                'base_document')
        if (request.GET.get('branch')):
            header_fields_dict['branch'] = request.GET.get('branch')
        if (request.GET.get('secondary_client')):
            if (request.GET.get('secondary_client') == 'current'
                ):  # special signal
                header_fields_dict[
                    'secondary_client'] = request.user.get_on_behalf_client()
            else:
                header_fields_dict['secondary_client'] = request.GET.get(
                    'secondary_client')

        return header_fields_dict
