'''
Created on 18/8/2016

@author: leobelen
'''
import json
import logging

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from antares.apps.core.middleware.request import get_request

from ..constants import FlowActivityStatusType, FlowPriorityType
from ..exceptions import FlowException
from ..manager import FlowManager
from ..models import FlowActivity, FlowUserNotificationOption


logger = logging.getLogger(__name__)


class WorkspaceView(TemplateView):
    template_name = 'workspace_view/workspace.html'

    def get_context_data(self, **kwargs):
        context = super(WorkspaceView, self).get_context_data(**kwargs)
        if 'activity_id' in kwargs:
            activity = FlowActivity.find_one(kwargs['activity_id'])
            if activity is None:
                raise FlowException(
                    _(__name__ + ".exceptions.no_activity_was_found"))
            if activity.performer != get_request().user:
                raise FlowException(
                    _(__name__ +
                      ".exceptions.this_activity_was_assigned_to_a_different_user"
                      ))
        else:
            raise FlowException(_(__name__ + ".no_activity_was_defined"))
        if activity.status == FlowActivityStatusType.CREATED:
            FlowManager.start_activity(activity)
        if (FlowUserNotificationOption.find_status_by_flow_case(
                activity.flow_case) == False):
            context['tracking_option'] = 'false'
        else:
            context['tracking_option'] = 'true'
        context['activity_tools'] = activity.process_tools()
        context['activity'] = activity
        context['performer'] = get_request().user
        context['priority_type_choices'] = json.dumps(
            FlowPriorityType.as_choices())

        return context
