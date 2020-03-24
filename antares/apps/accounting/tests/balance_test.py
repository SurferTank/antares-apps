'''
Created on Oct 2, 2017

@author: leobelen
'''
from antares.apps.document.constants import DocumentStatusType
from antares.apps.document.models import FormDefinition
from antares.apps.document.tests import DocumentTestHelper
from antares.apps.document.types import Document
import logging

from django.test import TransactionTestCase

from ..constants import BalanceStatusType, TransactionAffectedValueType
from ..manager import AccountManager
from ..models import AccountType, TransactionType, AccountRule


logger = logging.getLogger(__name__)


class BalanceTest(TransactionTestCase):
    """ Test the infrastructure to post a simple document """

    def setUp(self):
        self.docHelper = DocumentTestHelper()
        TransactionTestCase.setUp(self)

    def test_application(self):
        logger.info("Creating the form")
        self.docHelper.create_test_form_definition()
        
        logger.info("Creating the account type")
        accountType = AccountType()
        accountType.account_type_name = "Test Account"
        accountType.active = True
        accountType.description = "an account for testing purposes"
        accountType.save()
        
        logger.info("Transaction Type")
        debitTransactionType = TransactionType()
        debitTransactionType.active = True
        debitTransactionType.effect = BalanceStatusType.DEBIT
        debitTransactionType.calculate_charges = True
        debitTransactionType.description = "a debit transaction for testing purporses"
        debitTransactionType.save()
        
        logger.info("Account Rule creation")
        accountRule = AccountRule()
        accountRule.form_definition = FormDefinition.find_one("AccountForm-1")
        accountRule.amount_field = "anAmount"
        accountRule.value_affected = TransactionAffectedValueType.PRINCIPAL
        accountRule.transaction_type = debitTransactionType
        accountRule.save()

        logger.info("Document Creation")
        accdoc = Document(form_id="AccountForm-1")
        accdoc.set_field_value("aPeriod", 200101)
        accdoc.set_field_value("aAmount", 50)        
        accdoc.save(DocumentStatusType.DRAFTED)
        accountManager = AccountManager()
        accountManager.post_document(accdoc)
            
