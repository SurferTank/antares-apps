'''
Created on 16/8/2016

@author: leobelen
'''
import logging
import uuid

from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from antares.apps.client.models import Client
from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class AccountingPanelView(TemplateView):
    template_name = 'accounting_panel/accounting_panel.html'

    def get_context_data(self, **kwargs):
        context = super(AccountingPanelView, self).get_context_data(**kwargs)
        if ('is_inner' in self.request.GET):
            template = 'empty_layout.html'
            is_inner = True
        else:
            template = 'base_layout.html'
            is_inner = False
        if (self.request.GET.get('client_id')):
            client = Client.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
            # TODO: check validity
            if (client is None):
                messages.add_message(
                    self.request, messages.WARNING,
                    _(__name__ + '.exceptions.client_does_not_exist'))
                context['client'] = None
                context['template'] = template
                context['is_inner'] = is_inner
                return context

        else:
            try:
                client = get_request().user.get_on_behalf_client()
            except:
                messages.add_message(
                    self.request, messages.WARNING,
                    _(__name__ + '.exceptions.user_has_no_client_assigned {username}').\
                        format(username=self.request.user.username))
                context['client'] = None
                context['template'] = template
                context['is_inner'] = is_inner
                return context

        context['client'] = client
        context['template'] = template
        context['is_inner'] = is_inner

        return context
