import logging

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View

from ..models import FlowCase


logger = logging.getLogger(__name__)


class ApiCaseUpdateNameView(AjaxResponseMixin, JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        response_dict = {}
        case_id = request.POST.get('pk')
        value = request.POST.get('value')

        flow_case = FlowCase.find_one(case_id)
        if (flow_case is not None):
            flow_case.case_name = value
            flow_case.save()

        return self.render_json_response(response_dict)
