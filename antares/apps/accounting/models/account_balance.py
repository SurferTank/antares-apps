""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from enumfields import EnumField

from antares.apps.client.models.client import Client
from antares.apps.core.models.concept_type import ConceptType
from antares.apps.document.models.document_header import DocumentHeader

from ..constants import BalanceStatusType
from ..models.account_type import AccountType


logger = logging.getLogger(__name__)


class AccountBalance(models.Model):
    """ The current account balance record
    
    :attribute id: the account id
    :attribute default_currency: the currency in which the account is defined
    :attribute concept_type: the concept type for which the current account is defined
    :attribute compliance_document: the document  that marks the underlying obligation's compliance
    :attribute base_document: the document that created the account
    :attribute client: the client for which the account is created
    :attribute period: the period for which the account is created
    :attribute account_type: the account type for which the account is created
    :attribute balance_status: the balance status of the account
    :attribute calculation_date: last calculation date
    :attribute compliance_date: compliance date
    :attribute creation_date: creation date
    :attribute update: update date 
    :attribute interest_balance: total interest balance for the account
    :attribute principal_balance: total principal balance for the account
    :attribute penalties_balance: total penalties balance for the account
    :attribute total_balance: total balance for the account (principal+interest+penalties)
    :attribute hrn_code: human readable number for the account
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    default_currency = models.ForeignKey(
        "core.Currency",
        on_delete=models.PROTECT,
        db_column='default_currency',
        blank=True,
        null=True)
    concept_type = models.ForeignKey(
        "core.ConceptType",
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    compliance_document = models.ForeignKey(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='compliance_document',
        blank=True,
        null=True,
        related_name="account_document_compliance_document_set")
    base_document = models.ForeignKey(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='base_document',
        blank=True,
        null=True,
        related_name="account_document_base_document_set")
    client = models.ForeignKey(
        "client.Client", on_delete=models.PROTECT, db_column='client')
    account_type = models.ForeignKey(
        "AccountType", on_delete=models.PROTECT, db_column='account_type')

    balance_status = EnumField(
        BalanceStatusType, max_length=10, default=BalanceStatusType.BALANCED)

    calculation_date = models.DateTimeField()
    compliance_date = models.DateTimeField(blank=True, null=True)
    interest_balance = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=0)
    penalties_balance = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=0)
    period = models.IntegerField()
    principal_balance = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=0)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    total_balance = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=0)
    hrn_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_(__name__ + ".hrn_code"),
        help_text=_(__name__ + ".hrn_code_help"))

    def save(self, *args, **kwargs):
        """ Saves the balance after making some basic validations and sanity controls
        """
        from antares.apps.core.models import HrnCode
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.total_balance = self.principal_balance + \
            self.interest_balance + self.penalties_balance
        if not self.hrn_code:
            HrnCode.process_account_balance_hrn_script(self)
        super(AccountBalance, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.id)

    @classmethod
    def find_or_create_by_CCPAD(cls, client: Client, concept_type: ConceptType,
                                period: int, account_type: AccountType,
                                document: DocumentHeader):
        """ Returns the account balance that matches the unique identifiers - COPAD
        (Client, Concept type, Period, Account type and Document). If none is
        found, it creates one balance with zeroes as principal, interest, penalties and total. 
        
        """
        balance = AccountBalance.find_by_CCPAD(client, concept_type, period,
                                               account_type, document)
        if (balance is not None):
            return balance
        else:
            balance = AccountBalance()
            balance.account_type = account_type
            balance.client = client
            balance.status = str(BalanceStatusType)
            balance.principal_balance = Money(0, "USD")
            balance.interest_balance = Money(0, "USD")
            balance.penalties_balance = Money(0, "USD")
            balance.calculation_date = timezone.now()
            balance.creation_date = timezone.now()
            if (concept_type is not None):
                balance.concept_type = concept_type
            balance.period = period
            if (document is not None):
                balance.document = document
            balance.save()
            return balance

    @classmethod
    def find_by_CCPAD(cls, client: Client, concept_type: ConceptType,
                      period: int, account_type: AccountType,
                      document: DocumentHeader):
        """ Retrieves a balance by Client, concept type, Period, Account Type or, if a document based 
            document, by Client, Document, Period, Account type. It infers the document based account 
            based on the document being not none.
        """
        try:
            if (document is None):
                balance_list = list(
                    AccountBalance.objects.filter(
                        client=client,
                        concept_type=concept_type,
                        period=period,
                        account_type=account_type))
                if (len(balance_list) > 0):
                    return balance_list[0]
                else:
                    return None
            else:
                balance_list = list(
                    AccountBalance.objects.filter(
                        client=client,
                        document=document,
                        period=period,
                        account_type=account_type))
                if (len(balance_list) > 0):
                    return balance_list[0]
                else:
                    return None

        except AccountBalance.DoesNotExist:
            return None

    @classmethod
    def get_total_balance_by_client(cls, client: Client) -> float:
        """ Gets the total balance by client
        """
        if (client is None or client == ""):
            logger.info("The client is empty")
            return 0
        if isinstance(client, str):
            client = Client.find_one(uuid.UUID(client))
            if client is None:
                logger.info("The client was not found")
                return 0
        elif isinstance(client, uuid.UUID):
            client = Client.find_one(client)
            if (client is None):
                logger.info("The client was not found")
                return 0
        result = cls.objects.filter(client=client).exclude(
            account_type__exigible=False).aggregate(
                total_balance=models.Sum(models.F('total_balance')))
        return result['total_balance']

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_account_balance'
        #unique_together = (('client', 'concept_type', 'period', 'account_type',
        #                    'base_document', ), )
        unique_together = ((
            'client',
            'concept_type',
            'period',
            'account_type',
        ), )
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
