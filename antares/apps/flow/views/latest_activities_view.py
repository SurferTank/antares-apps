'''
Created on 18/8/2016

@author: leobelen
'''
import logging

from django.views.generic import TemplateView

from ..constants import FlowActivityStatusType


logger = logging.getLogger(__name__)


class LatestActivitiesView(TemplateView):
    template_name = 'latest_activities/latest_activities.html'