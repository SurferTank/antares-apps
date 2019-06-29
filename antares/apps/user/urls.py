from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .api import ApiOnBehalfChangeClientView
from .api import ApiOnBehalfSelectorView
from .views import AntaresAuthView

app_name = 'antares.apps.user'

urlpatterns = [
    url(r'^login$', AntaresAuthView.as_view(), name='account_login'),
    url(r'^logout$', LogoutView, name="account_logout"),
    url(r'^api/on_behalf_selector$',
        ApiOnBehalfSelectorView.as_view(),
        name="api_on_behalf_selector"),
    url(r'^api/on_behalf_change_client$',
        ApiOnBehalfChangeClientView.as_view(),
        name="api_on_behalf_change_client"),
]
