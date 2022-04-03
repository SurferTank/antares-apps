'''
Created on 16/8/2016

@author: leobelen
'''
from antares.apps.client.models import Client
from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import TemplateView


logger = logging.getLogger(__name__)


class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if ('is_inner' in self.request.GET):
            template = 'empty_layout.html'
            is_inner = True
        else:
            template = 'base_layout.html'
            is_inner = False

        context['template'] = template
        context['is_inner'] = is_inner
        return context
