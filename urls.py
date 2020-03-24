"""antares URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from antares.apps.accounting import urls as accountingUrls
from antares.apps.client import urls as clientUrls
from antares.apps.core import urls as coreUrls
from antares.apps.document import urls as documentUrls
from antares.apps.flow import urls as flowUrls
from antares.apps.obligation import urls as obligationUrls
from antares.apps.subscription import urls as subscriptionUrls
from antares.apps.terminal import urls as terminalUrls
from antares.apps.thirdparty import urls as thirdpartyUrls
from antares.apps.user import urls as user_urls

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve as staticServe


urlpatterns = i18n_patterns(
    url('^markdown/', include('django_markdown.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^antares/accounting/', include(accountingUrls)),
    url(r'^antares/client/', include(clientUrls)),
    url(r'^antares/core/', include(coreUrls)),
    url(r'^antares/document/', include(documentUrls)),
    url(r'^antares/flow/', include(flowUrls)),
    url(r'^antares/obligation/', include(obligationUrls)),
    # url(r'^antares/subscription/', include(subscriptionUrls)),
    url(r'^antares/terminal/', include(terminalUrls)),
    # url(r'^antares/thirdparty/', include(thirdpartyUrls)),
    url(r'^auth/', include(user_urls)),
    url(r'^static/(?P<path>.*)$', staticServe,
        {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', staticServe, {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^translation$',
        JavaScriptCatalog.as_view(domain="django"),
        name='js-catalog'),
    prefix_default_language=False)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += i18n_patterns(
        url(r'^__debug__/', include(debug_toolbar.urls)),
        prefix_default_language=False)
