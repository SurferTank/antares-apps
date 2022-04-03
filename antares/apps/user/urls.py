from django.urls import re_path
from django.contrib.auth.views import LogoutView

from .api import ApiOnBehalfChangeClientView
from .api import ApiOnBehalfSelectorView
from .views import AntaresAuthView


app_name = 'antares.apps.user'

urlpatterns = [
    re_path(r'^login$', AntaresAuthView.as_view(), name='account_login'),
    re_path(r'^logout$', LogoutView.as_view(), name="account_logout"),
    re_path(r'^api/on_behalf_selector$',
            ApiOnBehalfSelectorView.as_view(),
            name="api_on_behalf_selector"),
    re_path(r'^api/on_behalf_change_client$',
            ApiOnBehalfChangeClientView.as_view(),
            name="api_on_behalf_change_client"),
]
