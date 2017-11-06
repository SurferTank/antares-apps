'''
Created on Nov 5, 2017

@author: leobelen
'''
import logging

from django.test import TransactionTestCase
from ..service import MessageManager
from antares.apps.document.tests.document_test_helper import DocumentTestHelper

logger = logging.getLogger(__name__)


class TestMessageManager(TransactionTestCase):
    multi_db = True
    runs = 0
    message = """
    {
        "action": "create",
        "documents": [
            {
                "type": "account_form", 
                    "post_date": "2001-01-01T00:00:00+3",
                 "create_summary": false,
                "header": 
                    {
                        "period": 2001
                    }
                ,
            "fields": 
                {
                    "someVariableOnMessage": 100.1
                }
            }
        ]
    }
    """

    def setUp(self):
        TransactionTestCase.setUp(self)
        if self.runs == 0:
            self.doc_helper = DocumentTestHelper()
            self.runs = self.runs + 1

    def test_document_creation(self):
        self.doc_helper.create_test_form_definition()
        MessageManager.process_message(self.message)
