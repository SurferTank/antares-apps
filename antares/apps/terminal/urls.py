from django.urls import re_path
from django.contrib.auth.decorators import login_required

from .api import ApiRemoteTerminalView
from .views import RemoteTerminalView


app_name = 'antares.apps.terminal'

urlpatterns = [
    re_path(r'^$', login_required(
        RemoteTerminalView.as_view()), name="terminal"),
    re_path(r'^api$',
            login_required(ApiRemoteTerminalView.as_view()),
            name="terminal_ajax_call")
]
