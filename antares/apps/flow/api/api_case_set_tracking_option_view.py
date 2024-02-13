import logging

from antares.libs.braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View

from ..models import FlowCase, FlowUserNotificationOption


logger = logging.getLogger(__name__)


class ApiCaseSetTrackingOptionView(AjaxResponseMixin, JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        response_dict = {}
        case_id = request.POST.get('case_id')
        value = request.POST.get('value')

        flow_case = FlowCase.find_one(case_id)
        if flow_case is not None:
            option = FlowUserNotificationOption.find_or_create_one_by_flow_case(
                flow_case)
            if (value is not None
                    and (value.lower() == 'true' or value.lower() == 'yes')):
                option.active = True
            else:
                option.active = False
            option.save()

        return self.render_json_response(response_dict)
