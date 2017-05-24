from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .api import ApiBranchListAddressView
from .api import ApiBranchListBusinessClassificationView
from .api import ApiBranchListEmailView
from .api import ApiBranchListSocialNetworkView
from .api import ApiBranchListTelephoneView
from .api import ApiClientAttributesView
from .api import ApiClientIdView
from .api import ApiClientUserRelationsView
from .views import ClientPanelView

app_name = 'antares.apps.client'

urlpatterns = [
    url(r'^panel$',
        login_required(ClientPanelView.as_view()),
        name="panel_view"),
    url(r'^api/relations/view$',
        login_required(ApiClientUserRelationsView.as_view()),
        name="api_user_relations_view"),
    url(r'^api/attributes/view$',
        login_required(ApiClientAttributesView.as_view()),
        name="api_attributes_view"),
    url(r'^api/client_id/view$',
        login_required(ApiClientIdView.as_view()),
        name="api_client_id_view"),
    url(r'^api/addresses/view$',
        login_required(ApiBranchListAddressView.as_view()),
        name="api_branch_list_address_view"),
    url(r'^api/email/view$',
        login_required(ApiBranchListEmailView.as_view()),
        name="api_branch_list_email_view"),
    url(r'^api/email/view$',
        login_required(ApiBranchListBusinessClassificationView.as_view()),
        name="api_branch_list_business_classification_view"),
    url(r'^api/telephones/view$',
        login_required(ApiBranchListTelephoneView.as_view()),
        name="api_branch_list_telephone_view"),
    url(r'^api/socialnetworks/view$',
        login_required(ApiBranchListSocialNetworkView.as_view()),
        name="api_branch_list_social_network_view"),
]
