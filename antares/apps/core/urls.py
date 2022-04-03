from django.urls import re_path
from django.contrib.auth.decorators import login_required

from .api import ApiAutocompleteView
from .api import ApiSelectView
from .views import ProfileView


app_name = 'antares.apps.core'

urlpatterns = [
    re_path(r'api/select_options$',
            login_required(ApiSelectView.as_view()),
            name="api_select_options_view"),
    re_path(r'api/select_options$',
            login_required(ApiAutocompleteView.as_view()),
            name="api_autocomplete_options_view"),
    re_path(r'profile$',
            login_required(ProfileView.as_view()),
            name="profile_view"),


]
