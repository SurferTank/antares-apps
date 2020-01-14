from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .api import ApiAutocompleteView
from .api import ApiSelectView


app_name = 'antares.apps.core'

urlpatterns = [
    url(r'api/select_options$',
        login_required(ApiSelectView.as_view()),
        name="api_select_options_view"),
    url(r'api/select_options$',
        login_required(ApiAutocompleteView.as_view()),
        name="api_autocomplete_options_view"),
]
