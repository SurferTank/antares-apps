'''
Created on 16/8/2016

@author: leobelen
'''
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .api import ApiDocumentSubmitView
from .views import DocumentCreateView
from .views import DocumentEditView
from .views import DocumentViewView
from .api import ApiDocumentUploadView
from .api import ApiLatestDocumentView

app_name = 'antares.apps.document'

urlpatterns = [
    url(r'create/(?P<form_id>[\w\-]+)$',
        login_required(DocumentCreateView.as_view()),
        name="create_view"),
    url(r'edit/(?P<document_id>[\w\-]+)$',
        login_required(DocumentEditView.as_view()),
        name="edit_view"),
    url(r'view/(?P<document_id>[\w\-]+)$',
        login_required(DocumentViewView.as_view()),
        name="view_view"),
    url(r'api/edit$',
        login_required(ApiDocumentSubmitView.as_view()),
        name="api_edit_submit_view"),
    url(r'api/latest$',
        login_required(ApiLatestDocumentView.as_view()),
        name="api_latest_documents_view"),
    url(r'api/upload$',
        login_required(ApiDocumentUploadView.as_view()),
        name="api_upload_view"),
]
