'''
Created on 28 sep. 2016

@author: leobelen
'''
from copy import deepcopy

from antares.libs.braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View


class ApiOnBehalfSelectorView(AjaxResponseMixin, JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        response = []
        if 'q' in request.POST:
            client = {}
            client['id'] = str(request.user.client.id)
            client['text'] = request.user.client.code + ' - ' + \
                request.user.client.full_name
            response.append(deepcopy(client))
            for related_client in request.user.client_user_relation_set.select_related(
            ):
                client['id'] = str(related_client.child_client.id)
                client['text'] = related_client.child_client.code + ' - ' + \
                    related_client.child_client.full_name
                response.append(deepcopy(client))
        else:
            client = {}
            client['id'] = str(request.user.client.id)
            client['text'] = request.user.client.code + ' - ' + \
                request.user.client.full_name
            response.append(deepcopy(client))
            for related_client in request.user.client_user_relation_set.select_related(
            ):
                client['id'] = str(related_client.child_client.id)
                client['text'] = related_client.child_client.code + ' - ' + \
                    related_client.child_client.full_name
                response.append(deepcopy(client))
        return self.render_json_response(response)
