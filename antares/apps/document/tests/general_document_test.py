import logging

from django.test import TransactionTestCase

from ..types import Document
from antares.apps.document.constants import DocumentStatusType
from antares.apps.core.middleware import get_request
from .document_test_helper import DocumentTestHelper

logger = logging.getLogger(__name__)


class GeneralDocumentTest(TransactionTestCase):
    multi_db = True
    runs = 0

    def setUp(self):
        TransactionTestCase.setUp(self)
        if self.runs == 0:
            self.doc_helper = DocumentTestHelper()
            self.runs = self.runs + 1

    def test_form_class_creation(self):
        self.doc_helper.create_test_form_class()

    def test_form_definition_creation(self):
        self.doc_helper.create_test_form_definition()

    def test_document_creation(self):
        self.doc_helper.create_test_form_definition()
        document = Document(form_id=self.doc_helper.get_test_form_id())
        document.set_field_value("aPeriod", 200101)
        document.save(DocumentStatusType.DRAFTED)

        period = document.get_field_value("aPeriod")
        self.assertEqual(period, 200101, "Unexpected period found")
        document.set_author(get_request().user)
        document.save(DocumentStatusType.SAVED)
        #self.assertEqual(document.verify_hash_digest(), True , " Hash is incorrect for some reason")
