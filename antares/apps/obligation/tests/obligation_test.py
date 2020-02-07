'''
Created on Oct 2, 2017

@author: leobelen
'''
import logging
from django.test import TransactionTestCase
from antares.apps.document.tests import DocumentTestHelper

logger = logging.getLogger(__name__)



class BalanceTest(TransactionTestCase):
    """ Test the infrastructure to post a simple document """

    def setUp(self):
        self.docHelper = DocumentTestHelper()
        TransactionTestCase.setUp(self)

    def test_application(self):
        pass

            