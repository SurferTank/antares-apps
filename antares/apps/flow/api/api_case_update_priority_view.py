import logging

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import View

from antares.apps.core.middleware.request import get_request

from ..constants import FlowPriorityType
from ..models import FlowCase


logger = logging.getLogger(__name__)


class ApiCaseUpdatePriorityView(AjaxResponseMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        response_dict = {}
        case_id = request.POST.get('pk')
        value = request.POST.get('value')

        flow_case = FlowCase.find_one(case_id)
        if (flow_case is not None):
            priority = FlowPriorityType.to_enum(value)
            if (priority is not None):
                flow_case.priority = priority
                flow_case.save()

        return self.render_json_response(response_dict)
