from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .api import ApiCaseDocumentView
from .api import ApiCaseHistoryView
from .api import ApiCaseNoteListView
from .api import ApiCasePropertiesView
from .api import ApiCaseSetTrackingOptionView
from .api import ApiCaseUpdateNameView
from .api import ApiCaseUpdateNoteView
from .api import ApiCaseUpdatePriorityView
from .api import ApiCaseUpdatePropertyView
from .api import ApiForwardView
from .api import ApiInboxActiveCasesView
from .api import ApiInboxCompletedCasesView
from .api import ApiInboxCreatedCasesView
from .views import InboxView
from .views import LatestActivitiesView
from .views import WorkspaceView


app_name = 'antares.apps.flow'

urlpatterns = [
    #url(r'inbox/(?P<status_id>[\w\-]+)',
    #    login_required(InboxView.as_view()),
    #    name="inbox_view"),
    url(r'^inbox$', login_required(InboxView.as_view()), name="inbox_view"),
    url(r'^dashboard/(?P<activity_id>[\w\-]+)$',
        login_required(WorkspaceView.as_view()),
        name="dashboard_view"),
    url(r'^api/inbox/created/cases$',
        login_required(ApiInboxCreatedCasesView.as_view()),
        name="api_created_inbox_case_view"),
    url(r'^latest_activities$',
        login_required(LatestActivitiesView.as_view()),
        name="latest_activities_vew"),
    url(r'^api/inbox/active/cases$',
        login_required(ApiInboxActiveCasesView.as_view()),
        name="api_active_inbox_case_view"),
    url(r'^api/inbox/completed/cases$',
        login_required(ApiInboxCompletedCasesView.as_view()),
        name="api_completed_inbox_case_view"),
    url(r'^api/dashboard_forward_case$',
        login_required(ApiForwardView.as_view()),
        name="api_forward_case"),
    url(r'^api/dashboard_properties$',
        login_required(ApiCasePropertiesView.as_view()),
        name="api_case_properties"),
    url(r'^api/dashboard_history$',
        login_required(ApiCaseHistoryView.as_view()),
        name="api_case_history"),
    url(r'^api/dashboard_document$',
        login_required(ApiCaseDocumentView.as_view()),
        name="api_case_document"),
    url(r'^api/dashboard_update_property$',
        login_required(ApiCaseUpdatePropertyView.as_view()),
        name="api_case_update_property"),
    url(r'^api/dashboard_update_note$',
        login_required(ApiCaseUpdateNoteView.as_view()),
        name="api_case_update_note"),
    url(r'^api/dashboard_update_case_name$',
        login_required(ApiCaseUpdateNameView.as_view()),
        name="api_case_update_name"),
    url(r'^api/dashboard_update_case_priority$',
        login_required(ApiCaseUpdatePriorityView.as_view()),
        name="api_case_update_priority"),
    url(r'^api/dashboard_note_list$',
        login_required(ApiCaseNoteListView.as_view()),
        name="api_case_note_list"),
    url(r'^api/dashboard_set_tracking_option$',
        login_required(ApiCaseSetTrackingOptionView.as_view()),
        name="api_case_set_tracking_option"),
]
