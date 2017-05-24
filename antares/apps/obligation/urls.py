from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .api import ApiObligationPanelPendingView
from .api import ApiObligationPanelCompliedView
from .views import ObligationPanelView

app_name = 'antares.apps.obligation'

urlpatterns = [
    url(r'panel/(?P<client_id>[\w\-]+)$',
        login_required(ObligationPanelView.as_view()),
        name="panel_view_client"),
    url(r'panel$',
        login_required(ObligationPanelView.as_view()),
        name="panel_view"),
    url(r'ajax/call/pending$',
        login_required(ApiObligationPanelPendingView.as_view()),
        name="panel_ajax_pending_view"),
    url(r'ajax/call/compliant$',
        login_required(ApiObligationPanelCompliedView.as_view()),
        name="panel_ajax_complied_view"),
]
