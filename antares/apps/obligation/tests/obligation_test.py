'''
Created on Oct 2, 2017

@author: leobelen
'''
from antares.apps.document.tests import DocumentTestHelper
import logging

from django.test import TransactionTestCase

from ..models import ObligationRule


logger = logging.getLogger(__name__)


class BalanceTest(TransactionTestCase):
    """ Test the infrastructure to post a simple document """

    def setUp(self):
        self.docHelper = DocumentTestHelper()
        TransactionTestCase.setUp(self)

    def test_obligationRule(self):
        obligationRule = ObligationRule()

        pass
            
