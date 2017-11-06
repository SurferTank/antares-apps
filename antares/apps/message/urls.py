from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from rest_framework.urlpatterns import format_suffix_patterns

from .api import MessageApi
from .api import MessageDetailsApi


app_name = 'antares.apps.message'

urlpatterns = [
   url(r'api/message', MessageApi.as_view(),
        name="api_message"),
    url(r'api/message/(?P<pk>[0-9][a-z][A-Z]+)/$', MessageDetailsApi.as_view(),
        name="api_message_details"),
]

urlpatterns = format_suffix_patterns(urlpatterns)