'''
Created on Jun 21, 2016

@author: leobelen
'''
import logging

from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.client.models import Client
from antares.apps.core.constants import FieldDataType
from antares.apps.core.models import ConceptType
from antares.apps.core.models import SystemParameter
from antares.apps.document.types import Document

from ..constants import AccountDocumentStatusType
from ..constants import TransactionEffectType, TransactionAffectedValueType, BalanceStatusType
from ..exceptions import MissingAccountHeaderInformationException, NegativeAmountException
from ..models import AccountBalance
from ..models import AccountDocument
from ..models import AccountRule
from ..models import AccountTransaction
from ..models import AccountType

logger = logging.getLogger(__name__)


class AccountManager(object):
    '''
    
    '''

    def __init__(self):
        pass

    @classmethod
    def post_document(cls, document: Document):
        account_rules = AccountRule.find_active_by_form_definition(
            document.header.form_definition)
        if (len(account_rules) == 0):
            logger.info(_(__name__ + '.no_rules_found'))
            return

        account_document = AccountDocument.find_or_create_by_document(
            document.header)

        if (account_document.status != AccountDocumentStatusType.PENDING):
            logger.error(_(__name__ + '.document_not_ready_for_posting'))
            return

        # try:
        cancelled_document = AccountManager._get_cancelled_document(document)
        if (cancelled_document is not None):
            logger.error(
                _(__name__ + '.cancelling_document %(document_id)s') %
                {'document_id': document.document_id})
            AccountManager._cancel_document(cancelled_document, document)

        transactions = AccountManager._create_transactions_from_rules(
            account_document, document, account_rules)

        account_document.content = AccountManager._get_account_document_string(
            account_document, transactions)
        account_document.status = AccountDocumentStatusType.PROCESSED

        # except Exception:
        #    account_document.status = str(AccountDocumentStatusType.WITH_ERRORS)
        account_document.save()

    @classmethod
    def _get_account_document_string(cls, account_document, transactions):
        return None

    @classmethod
    def _get_cancelled_document(cls, document):
        return None

    @classmethod
    def _cancel_document(cls, cancelled_document, document):
        pass

    @classmethod
    def _create_transactions_from_rules(cls, account_document, document,
                                        account_rules):
        """
        This function processes the rules one by one and tries to produce the transactions.
        """
        transaction_list = []
        for rule in account_rules:
            transaction = AccountManager._create_transaction(
                account_document, document, rule)
            if (AccountManager._is_transaction_to_be_applied(transaction)):
                transaction_list.append(transaction)
                AccountManager._apply_transaction_to_balance(
                    transaction, document)
        return transaction_list

    @classmethod
    def _create_transaction(cls, account_document, document, rule):
        default_payment_transaction = SystemParameter.find_one(
            "DEFAULT_PAYMENT_TRANSACTION_TYPE", FieldDataType.STRING,
            'PAYMENT')
        """
        Computes the transaction out of a document and a rule
        """
        transaction = AccountTransaction()
        transaction.document = account_document.document
        transaction.account_document = account_document
        transaction.creation_date = timezone.now()
        transaction.transaction_date = timezone.now()
        transaction.posted_date = timezone.now()
        transaction.client = AccountManager._process_client(
            account_document, document, rule)
        transaction.account_type = AccountManager._process_account_type(
            account_document, document, rule)
        transaction.concept_type = AccountManager._process_concept_type(
            account_document, document, rule)
        transaction.period = AccountManager._process_period(
            account_document, document, rule)
        transaction.transaction_type = AccountManager._process_transaction_type(
            account_document, document, rule)
        transaction = AccountManager._process_amount(
            account_document, document, rule, transaction, False)
        if (transaction.transaction_type.id == default_payment_transaction):
            transaction = AccountManager._process_payment_transaction(
                transaction, document)

        transaction.balance = AccountBalance.find_or_create_by_CCPAD(
            transaction.client, transaction.concept_type, transaction.period,
            transaction.account_type, None)
        transaction.save()
        return transaction

    @classmethod
    def _process_payment_transaction(cls, transaction, document):
        """
        We need this one.
        """
        paymentApplicationMethod = SystemParameter.find_one(
            "DEFAULT_PAYMENT_APPLICATION_METHOD", FieldDataType.STRING,
            'PRINCIPAL_INTEREST_PENALTIES')

    @classmethod
    def _is_transaction_to_be_applied(cls, transaction):
        if (transaction.transaction_type.post_zeros == True or
                transaction.total_amount > 0):
            return True
        else:
            return False

    @classmethod
    def _apply_transaction_to_balance(cls, transaction, document):
        logger.info(
            _(__name__ +
              ".manager.account_manager.starting_to_balance_the_account"))
        principal = 0
        interest = 0
        penalties = 0

        transaction_list = AccountTransaction.find_by_balance(
            transaction.balance)
        if (len(transaction_list) == 0):
            return

        for trans in transaction_list:
            if (trans.transaction_type.effect == TransactionEffectType.CREDIT):
                principal = principal + transaction.principal_amount
                interest = interest + transaction.interest_amount
                penalties = penalties + transaction.penalties_amount
            elif (trans.transaction_type.effect ==
                  TransactionEffectType.DEBIT):
                principal = principal - transaction.principal_amount
                interest = interest - transaction.interest_amount
                penalties = penalties - transaction.penalties_amount

        logger.info(
            _('antares.app.accounting.manager.apply_transaction_to_balance_info1 %(principal)d %(interest)d %(penalties)d'
              ) % {
                  'principal': principal,
                  'interest': interest,
                  'penalties': penalties
              })

        transaction.balance.principal_balance = principal
        transaction.balance.interest_balance = interest
        transaction.balance.penalties_balance = penalties
        transaction.balance.balance_status = str(
            AccountManager._compute_balance_status(principal, interest,
                                                   penalties))
        transaction.balance.save()

    @classmethod
    def _compute_balance_status(cls, principal, interest, penalties):
        total = principal + interest + penalties
        if (total == 0):
            return BalanceStatusType.BALANCED
        elif (total > 0):
            return BalanceStatusType.CREDIT
        else:
            return BalanceStatusType.DEBIT

    @classmethod
    def _process_client(cls, account_document, document, rule):
        if rule.client_id_field:
            client_id = document.get_field_value(rule.client_id_field)
            if (client_id is not None):
                client = Client.find_one(client_id)
                if (client is not None):
                    return client
        elif rule.fixed_client is not None:
            return rule.fixed_client
        elif document.get_client() is not None:
            return document.get_client()
        else:
            raise MissingAccountHeaderInformationException(
                _(__name__ + ".manager.account_manager.missing_client"))

    @classmethod
    def _process_account_type(cls, account_document, document, rule):
        if (rule.account_type is not None):
            return rule.account_type
        elif (rule.account_type_field is not None):
            account_type_field = document.get_field_value(
                rule.account_type_field)
            if (account_type_field is not None):
                account_type = AccountType.find_one(account_type_field)
                if (account_type is not None):
                    return account_type
        elif (account_document.document.get_account_type() is not None):
            return account_document.document.get_account_type()
        else:
            raise MissingAccountHeaderInformationException(
                _(__name__ + ".manager.account_manager.missing_account_type"))

    @classmethod
    def _process_concept_type(cls, account_document, document, rule):
        if (rule.concept_type is not None):
            return rule.concept_type
        elif (rule.concept_type_field is not None):
            concept_type_field = document.get_field_value(
                rule.concept_type_field)
            if (concept_type_field is not None):
                concept_type = ConceptType.find_one(concept_type_field)
                if (concept_type is not None):
                    return concept_type
        elif (account_document.document.get_concept_type() is not None):
            return account_document.document.get_concept_type()
        else:
            raise MissingAccountHeaderInformationException(
                _(__name__ + ".manager.account_manager.missing_concept_type"))

    @classmethod
    def _process_period(cls, account_document, document, rule):
        if (rule.fixed_period or rule.fixed_period != 0):
            return rule.fixed_period
        else:
            period = int(float(document.get_field_value(rule.period_field)))
            if (period):
                return period
            else:
                raise MissingAccountHeaderInformationException(
                    _(__name__ + ".manager.account_manager.missing_period"))

    @classmethod
    def _process_transaction_type(cls, account_document, document, rule):
        return rule.transaction_type

    @classmethod
    def _process_amount(cls,
                        account_document,
                        document,
                        rule,
                        transaction,
                        is_cancelled_document=False):
        field_value = float(document.get_field_value(rule.amount_field))
        value_affected = rule.value_affected
        if field_value is None:
            field_value = 0
        if field_value < 0:
            raise NegativeAmountException(
                _(__name__ + ".exceptions.negative_amount_exception"))

        if not is_cancelled_document:
            if value_affected == TransactionAffectedValueType.PRINCIPAL:
                transaction.principal_amount = field_value
                transaction.interest_amount = 0
                transaction.penalties_amount = 0
            elif value_affected == TransactionAffectedValueType.INTEREST:
                transaction.principal_amount = 0
                transaction.interest_amount = field_value
                transaction.penalties_amount = 0
            elif value_affected == TransactionAffectedValueType.PENALTIES:
                transaction.principal_amount = 0
                transaction.interest_amount = 0
                transaction.penalties_amount = field_value
        else:
            raise NotImplementedError

        transaction.total_amount = transaction.principal_amount + \
            transaction.interest_amount + transaction.penalties_amount
        return transaction
