'''
Created on 29 sep. 2016

@author: leobelen
'''
from antares.apps.client.models import Client
import uuid

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic import View


class ApiOnBehalfChangeClientView(AjaxResponseMixin, JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        response = []
        if 'client_id' in request.POST:
            client = Client.find_one(uuid.UUID(request.POST.get('client_id')))
            if (client is not None):
                request.user.set_on_behalf_client(client)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _(__name__ + ".client_successfully_changed {client}")
                    .format(client=client.code + ' - ' + client.full_name))
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(__name__ + ".client_was_not_found {client}").format(
                        client=request.POST.get('client_id')))
        else:
            messages.add_message(request, messages.ERROR,
                                 _(__name__ + ".no_client_was_specified"))

        return self.render_json_response(response)
