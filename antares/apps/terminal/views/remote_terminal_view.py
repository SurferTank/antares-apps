import logging

from django.views.generic import TemplateView

from antares.apps.user.decorators import role_required


logger = logging.getLogger(__name__)


class RemoteTerminalView(TemplateView):
    template_name = 'remote_terminal/remote_terminal.html'

    @role_required("FLOW_DEFAULT_ROLE")
    def dispatch(self, request, *args, **kwargs):
        return super(RemoteTerminalView, self).dispatch(
            request, *args, **kwargs)
