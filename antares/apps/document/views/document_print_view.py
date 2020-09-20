'''
Created on 16/8/2016

@author: leobelen
'''

from antares.apps.accounting.models import AccountType
from antares.apps.client.models import Client
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import ConceptType
import logging
import uuid

from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import View

from ..constants import FormDefinitionStatusType
from ..types import Document


logger = logging.getLogger(__name__)


class DocumentPrintView(TemplateView):
    """
    Handles the interface to create and edit new documents.
    """

    def __init__(self):
        pass

    def get(self, request, document_id):

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
            # TODO: this should be decided first.
            next_place = '/home'

        # TODO: Auth is missing here

        document = Document(document_id=document_id)
        document.set_author(get_request().user)

        if ('client' in request.GET):
            client = Client.find_one(uuid.UUID(request.GET.get('client')))
            if (client is not None):
                document.set_client(client)

        if ('concept_type' in request.GET):
            concept_type = ConceptType.find_one(
                uuid.UUID(request.GET.get('concept_type')))
            if (concept_type is not None):
                document.set_concept_type(concept_type)
        if ('period' in request.GET):
            document.set_period(request.GET.get('period'))

        if ('account_type' in request.GET):
            account_type = ConceptType.find_one(
                uuid.UUID(request.GET.get('account_type')))
            if (account_type is not None):
                document.set_account_type(account_type)

        if ('secondary_client' in request.GET):
            secondary_client = Client.find_one(
                uuid.UUID(request.GET.get('secondary_client')))
            if (secondary_client is not None):
                document.set_secondary_client(secondary_client)

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
