'''
Created on 18/8/2016

@author: leobelen
'''
import logging

from django.views.generic import TemplateView

from ..constants import FlowActivityStatusType

logger = logging.getLogger(__name__)


class InboxView(TemplateView):
    template_name = 'inbox_view/inbox.html'

    def __init_(self):
        logger.info("we are here!")

    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data(**kwargs)

        context['activity_status'] = FlowActivityStatusType.CREATED
        return context
