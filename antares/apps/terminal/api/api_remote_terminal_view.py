from antares.apps.accounting.console import AccountConsole
from antares.apps.client.console import ClientUserRelationConsole
from antares.apps.core.console import ConceptTypeConsole
from antares.apps.core.console import NukeConsole
from antares.apps.document.console import DocumentConsole
from antares.apps.flow.console import FlowAdminConsole
from antares.apps.initialsettings.console import InitialSettingsConsole
from antares.apps.initialsettings.console import IsicConsole
from antares.apps.notifications.console import NotificationConsole
from antares.apps.obligation.console import ObligationConsole
from antares.apps.subscription.console import SubscriptionConsole
from antares.apps.user.console import UserConsole
import logging
import re
import traceback

from antares.libs.braces.views import AjaxResponseMixin, JSONResponseMixin
from django.utils.translation import gettext as _
from django.views.generic import View

from ..models import TerminalLog


logger = logging.getLogger(__name__)


class ApiRemoteTerminalView(AjaxResponseMixin, JSONResponseMixin, View):
    action_regex_pattern = '(\\S+):(?:"((?:\\"|[^"])+)"|(\\S+))|(\\S+)'

    def post_ajax(self, request, *args, **kwargs):
        action_list = request.POST.get('action[]').split(';')
        # default value for message
        message = ''

        for action in action_list:
            commands = self.parse_action(action)
            message += self.process_commands(commands, True)

        TerminalLog.log_terminal(request.POST.get('action[]'), message)
        response_dict = {'message': message}
        return self.render_json_response(response_dict)

    def parse_action(self, action):
        commands = {}
        matches = re.findall(self.action_regex_pattern, action)
        for match in matches:
            if match[0] is not '' and match[2] is not '':
                commands[match[0].lower()] = match[2]
            elif match[0] is not '' and match[3] is not '':
                commands[match[0].lower()] = match[3]
            elif match[3] is not '':
                commands[match[3].lower()] = ''
        return commands

    def process_commands(self, params, html=False):
        message = ""
        try:
            if ('document' in params):
                message += DocumentConsole.process_commands(params, html)
            elif ('account' in params):
                message += AccountConsole.process_commands(params, html)
            elif ('flow' in params):
                message += FlowAdminConsole.process_commands(params, html)
            elif ('subscription' in params):
                message += SubscriptionConsole.process_commands(params, html)
            elif ('concepttype' in params):
                message += ConceptTypeConsole.process_commands(params, html)
            elif ('obligation' in params):
                message += ObligationConsole.process_commands(params, html)
            elif ('clientrelation' in params):
                message += ClientUserRelationConsole.process_commands(
                    params, html)
            elif ('nuke' in params):
                message += NukeConsole.process_commands(params, html)
            elif ('isic' in params):
                message += IsicConsole.process_commands(params, html)
            elif ('notification' in params):
                message += NotificationConsole.process_commands(params, html)
            elif ('initialsettings' in params):
                message += InitialSettingsConsole.process_commands(
                    params, html)
            elif ('user' in params):
                message += UserConsole.process_commands(params, html)
            else:
                message = _(__name__ + '.messages.no_action_taken')

        except Exception as exception:
            message += str(
                exception) + '<br /><pre>' + traceback.format_exc() + "</pre>"
        return message
