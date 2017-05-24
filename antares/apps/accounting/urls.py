'''
Created on 16/8/2016

@author: leobelen
'''
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .api import ApiAccountTypeView
from .api import ApiClientView
from .api import ApiConceptTypeView
from .api import ApiPeriodView
from .views import AccountingPanelView

app_name = 'antares.apps.accounting'

urlpatterns = [
    url(r'^panel$',
        login_required(AccountingPanelView.as_view()),
        name="panel_view"),
    url(r'^api/panel/by_client_concept_type$',
        ApiClientView.as_view(),
        name="api_client"),
    url(r'^api/panel/by_concept_type$',
        ApiConceptTypeView.as_view(),
        name="api_concept_type"),
    url(r'^api/panel/by_period$', ApiPeriodView.as_view(), name="api_period"),
    url(r'^api/panel/by_account_type$',
        ApiAccountTypeView.as_view(),
        name="api_account_type"),
]
