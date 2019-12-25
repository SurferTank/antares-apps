import logging
import uuid

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.utils.translation import ugettext as _
from django.views.generic import View

from ..models import FlowCase, FlowProperty


logger = logging.getLogger(__name__)


class ApiCaseUpdatePropertyView(AjaxResponseMixin, JSONResponseMixin, View):
    def post(self, request):
        response_dict = {}
        if 'case_id' in request.POST:
            flow_case = FlowCase.find_one(
                uuid.UUID(request.POST.get('case_id')))
            if flow_case is None:
                raise ValueError(_(__name__ + ".flow_case_does_not_exist"))
        if 'property_id' in request.POST:
            flow_property = FlowProperty.find_one_by_flow_case_and_property_id(
                flow_case, request.POST.get('property_id'))
            if flow_property is None:
                raise ValueError(_(__name__ + ".property_does_not_exist"))
        if 'property_value' in request.POST:
            flow_property.update_property_with_value(
                request.POST.get('property_value'))

        return self.render_json_response(response_dict)
