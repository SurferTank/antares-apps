from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .api import ApiRemoteTerminalView
from .views import RemoteTerminalView

app_name = 'antares.apps.terminal'

urlpatterns = [
    url(r'^$', login_required(RemoteTerminalView.as_view()), name="terminal"),
    url(r'^api$',
        login_required(ApiRemoteTerminalView.as_view()),
        name="terminal_ajax_call")
]
