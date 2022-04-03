from django.urls import re_path
from django.contrib.auth.decorators import login_required

from .api import ApiObligationPanelCompliedView
from .api import ApiObligationPanelPendingView
from .views import ObligationPanelView


app_name = 'antares.apps.obligation'

urlpatterns = [
    re_path(r'panel/(?P<client_id>[\w\-]+)$',
            login_required(ObligationPanelView.as_view()),
            name="panel_view_client"),
    re_path(r'panel$',
            login_required(ObligationPanelView.as_view()),
            name="panel_view"),
    re_path(r'ajax/call/pending$',
            login_required(ApiObligationPanelPendingView.as_view()),
            name="panel_ajax_pending_view"),
    re_path(r'ajax/call/compliant$',
            login_required(ApiObligationPanelCompliedView.as_view()),
            name="panel_ajax_complied_view"),
]
