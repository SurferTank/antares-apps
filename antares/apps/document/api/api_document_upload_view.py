'''
Created on 16/8/2016

@author: leobelen
'''

import json
import logging

from braces.views import AjaxResponseMixin, JSONResponseMixin
import dateutil.parser
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views.generic import View

from antares.apps.core.middleware.request import get_request
from antares.apps.user.models import User

from ..constants import DocumentStatusType
from ..models import FormDefinition
from ..types import Document


logger = logging.getLogger(__name__)

test_document = "/docs/projects/www/antares/antares/apps/document/xml/working/upload_document.json"


class ApiDocumentUploadView(AjaxResponseMixin, JSONResponseMixin, View):
    '''
    classdocs
    '''

    def get(self, request, *args, **kwargs):
        response_dict = {}
        with open(test_document, "r") as myfile:
            json_file = myfile.read()
        json_document = json.loads(json_file)
        form_definition = FormDefinition.find_one_by_third_party_type(
            json_document["general"]['type'])
        if form_definition is None:
            response_dict["status"] = "Error"
            response_dict["message"] = _(__name__ +
                                         ".errors.no_form_definition_found")

        author = User.find_one_by_username(json_document["general"]["author"])
        if author is None:
            response_dict["status"] = "Error"
            response_dict["message"] = _(__name__ + ".errors.no_author_found")

        creation_date = dateutil.parser.parse(
            json_document["general"]["creation_date"])
        if creation_date is None:
            creation_date = timezone.now()

        for doc_fields in json_document["documents"]:
            document = Document(form_id=form_definition)
            document.set_creation_date(creation_date)
            document.set_author(author)
            for key, value in doc_fields.items():
                doc_id = document.get_field_id_by_messagemap(key)
                document.set_field_value(doc_id, value)
            document.save(DocumentStatusType.SAVED)

        response_dict["status"] = "OK"
        response_dict["document_id"] = document.document_id
        response_dict["message"] = _(__name__ + ".document_created")

        return self.render_json_response(response_dict)
