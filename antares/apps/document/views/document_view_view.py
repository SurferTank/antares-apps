'''
Created on 16/8/2016

@author: leobelen
'''

import logging

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View

from ..types import Document


logger = logging.getLogger(__name__)


class DocumentViewView(View):
    '''
    classdocs
    '''

    def get(self, request, document_id):
        # TODO: Auth is missing here

        document = Document(document_id=document_id)
        if ('is_inner' in request.GET):
            template = 'empty_layout.html'
            is_inner = 'true'
        else:
            template = 'base_layout.html'
            is_inner = 'false'

        if ('next' in request.GET):
            next_place = request.GET.get('next')
        else:
            next_place = None

        document.get_form_definition().verify_and_create_supporting_files(
            settings.DEBUG)

        return render(
            request,
            document.get_form_definition().get_view_site_path(), {
                'document': document.header,
                'headerFields': document.get_header_field_dict(),
                'fields': document.get_field_dict(),
                'template': template,
                'next_place': next_place,
                'is_inner': is_inner,
            })
