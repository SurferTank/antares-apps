'''
Created on 19/8/2016

@author: leobelen
'''
import logging
import uuid

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from django.contrib import messages

from antares.apps.client.models import Client
from antares.apps.core.middleware.request import get_request
from antares.apps.flow.models import FlowActivity

logger = logging.getLogger(__name__)


class ObligationPanelView(TemplateView):
    template_name = 'obligation_panel/obligation_panel.html'

    def get_context_data(self, **kwargs):
        context = super(ObligationPanelView, self).get_context_data(**kwargs)
        if self.request.GET.get('activity_id'):
            activity = FlowActivity.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
            if (activity is None):
                messages.add_message(
                    self.request, messages.INFO,
                    _(__name__ + ".exceptions.activity_not_found"))
        else:
            activity = None
        if self.request.GET.get('client_id'):
            client = Client.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
            # TODO: check validity
            if (client is None):
                messages.add_message(
                    self.request, messages.INFO,
                    _(__name__ + ".exceptions.client_not_found"))

        else:
            client = get_request().user.get_on_behalf_client()
            if (client is None):
                messages.add_message(
                    self.request, messages.INFO,
                    _(__name__ + ".exceptions.user_has_no_client_assigned"))

        if ('is_inner' in self.request.GET):
            template = 'empty_layout.html'
            is_inner = True
        else:
            template = 'base_layout.html'
            is_inner = False

        context['activity'] = activity
        context['client'] = client
        context['template'] = template
        context['is_inner'] = is_inner

        return context
