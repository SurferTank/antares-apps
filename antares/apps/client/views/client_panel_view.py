'''
Created on 16/8/2016

@author: leobelen
'''
import logging
import uuid

from django.contrib import messages
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from antares.apps.user.exceptions import UserException

from ..models import Client


logger = logging.getLogger(__name__)


class ClientPanelView(TemplateView):
    '''
    classdocs
    '''
    template_name = 'client_panel/client_panel.html'

    def get_context_data(self, **kwargs):
        context = super(ClientPanelView, self).get_context_data(**kwargs)
        if ('is_inner' in self.request.GET):
            template = 'empty_layout.html'
            is_inner = True
        else:
            template = 'base_layout.html'
            is_inner = False
        if (self.request.GET.get('client_id')):
            client = Client.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
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
                client = self.request.user.get_on_behalf_client()
            except UserException:
                messages.add_message(
                    self.request, messages.WARNING, _(__name__ + '.exceptions.user_has_no_client_assigned {username}').\
                        format(username=self.request.user.username))
                context['client'] = None
                context['template'] = template
                context['is_inner'] = is_inner
                return context

        main_branch = client.branch_set.select_related().get(branch_number=0)
        branches = client.branch_set.select_related().exclude(branch_number=0)

        context['client'] = client
        context['main_branch'] = main_branch
        context['branches'] = branches
        context['template'] = template
        context['is_inner'] = is_inner
        return context
