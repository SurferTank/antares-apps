'''
Created on 21/8/2016

@author: leobelen
'''
from antares.apps.core.models.catalog import Catalog
import logging

from antares.libs.braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View


logger = logging.getLogger(__name__)


class ApiSelectView(AjaxResponseMixin, JSONResponseMixin, View):

    def get(self, request, *args, **kwargs):
        if 'selector' in request.GET:
            if 'q' in request.GET:
                element_list = Catalog.find_list_by_catalog_id(
                    request.GET.get('selector'), request.GET.get('q'))
            else:
                element_list = Catalog.find_list_by_catalog_id(
                    request.GET.get('selector'))
        return self.render_json_response(element_list)
