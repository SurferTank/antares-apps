'''
Created on 16/8/2016

@author: leobelen
'''
from django.urls import re_path
from django.contrib.auth.decorators import login_required

from .api import ApiDocumentSubmitView
from .api import ApiDocumentUploadView
from .api import ApiLatestDocumentView
from .views import DocumentCreateView
from .views import DocumentEditView
from .views import DocumentViewView
from .views import DocumentPrintView


app_name = 'antares.apps.document'

urlpatterns = [
    re_path(r'create/(?P<form_id>[\w\-]+)$',
            login_required(DocumentCreateView.as_view()),
            name="create_view"),
    re_path(r'edit/(?P<document_id>[\w\-]+)$',
            login_required(DocumentEditView.as_view()),
            name="edit_view"),
    re_path(r'view/(?P<document_id>[\w\-]+)$',
            login_required(DocumentViewView.as_view()),
            name="view_view"),
    re_path(r'view/(?P<document_id>[\w\-]+)$',
            login_required(DocumentPrintView.as_view()),
            name="print_view"),
    re_path(r'api/edit$',
            login_required(ApiDocumentSubmitView.as_view()),
            name="api_edit_submit_view"),
    re_path(r'api/latest$',
            login_required(ApiLatestDocumentView.as_view()),
            name="api_latest_documents_view"),
    re_path(r'api/upload$',
            login_required(ApiDocumentUploadView.as_view()),
            name="api_upload_view"),
]
