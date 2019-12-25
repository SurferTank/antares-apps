import logging

from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.views.generic import View

from ..manager import FlowManager
from ..models import FlowActivity


logger = logging.getLogger(__name__)


class ApiForwardView(AjaxResponseMixin, JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        response_dict = {}
        request_type = request.POST.get('type')
        if 'activityId' in request.POST:
            activity = FlowActivity.find_one(request.POST.get('activityId'))
        if (request.POST.get('confirmation').lower() == 'yes'
                or request.POST.get('confirmation').lower() == 'true'):
            confirmation = True
        else:
            confirmation = False

        if request_type.lower() == 'forward':
            result = FlowManager.forward_activity(activity, None, confirmation)
            if (result is not None and len(result) != 0
                    and confirmation == False):
                return self.render_json_response(result)
            else:
                return self.render_json_response("")

        return self.render_json_response(response_dict)
