import logging

from django.test import TestCase

logger = logging.getLogger(__name__)

class GeneralDocumentTest(TestCase):
    
    def test_document_creation(self):
        print("we are testing if a document can be created")