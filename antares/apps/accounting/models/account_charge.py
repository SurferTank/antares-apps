""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""
from antares.apps.client.models.client import Client
from antares.apps.core.models.concept_type import ConceptType
from antares.apps.document.models.document_header import DocumentHeader
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from ..constants import TransactionAffectedValueType
from .account_type import AccountType
from .interest_definition import InterestDefinition
from .penalty_definition import PenaltyDefinition


logger = logging.getLogger(__name__)


class AccountCharge(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    concept_type = models.ForeignKey(
        ConceptType,
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    base_document = models.ForeignKey(
        DocumentHeader,
        on_delete=models.PROTECT,
        db_column='base_document',
        blank=True,
        null=True,
        related_name="account_charge_base_document_set")
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, db_column='client')
    account_type = models.ForeignKey(
        AccountType, on_delete=models.PROTECT, db_column='account_type')
    period = models.IntegerField(blank=False, null=False)
    charge_period = models.IntegerField(blank=False, null=False)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    amount = MoneyField(
        max_digits=15, decimal_places=2, default_currency='USD', default=0, null=False, blank=False, editable=False)
    interest_definition = models.ForeignKey(
        InterestDefinition,
        on_delete=models.PROTECT,
        db_column='interest_definition',
        blank=True,
        null=True,
        related_name="account_charge_interest_definition_set")
    penalty_definition = models.ForeignKey(
        PenaltyDefinition,
        on_delete=models.PROTECT,
        db_column='penalty_definition',
        blank=True,
        null=True,
        related_name="account_charge_penalty_definition_set")
    charge_document = models.ForeignKey(
        DocumentHeader,
        on_delete=models.PROTECT,
        db_column='charge_document',
        blank=True,
        null=True,
        related_name="account_charge_document_set")
    
    def save(self, *args, **kwargs):
        """ 
        Saves the balance after making some basic validations and sanity controls
        """
        self.creation_date = timezone.now()
        super(AccountCharge, self).save(*args, **kwargs)

    def setCOPADPeriodInterestDefinition(self, copad, period, interestDefinition):
        self.client = copad.client
        self.concept_type = copad.concept_type
        self.period = copad.period 
        self.account_type = copad.account_type
        self.base_document = copad.base_document 
        self.charge_period = period
        self.interest_definition = interestDefinition
    
    def setCOPADPeriodPenaltyDefinition(self, copad, period, penaltyDefinition):
        self.client = copad.client
        self.concept_type = copad.concept_type
        self.period = copad.period 
        self.account_type = copad.account_type
        self.base_document = copad.base_document 
        self.charge_period = period
        self.penalty_definition = penaltyDefinition
        
    @classmethod
    def findByCOPAD(cls, copad):
        try:
            return AccountCharge.objects.get(
                client=copad.client,
                concept_type=copad.concept_type,
                period=copad.period,
                account_type=copad.account_type,
                base_document=copad.base_document)
        except AccountCharge.DoesNotExist:
            return None
        
    @classmethod
    def findByCOPADChargePeriodAndInterestDefinition(cls, copad, period, interestDefinition):
        try:
            return AccountCharge.objects.get(
                client=copad.client,
                concept_type=copad.concept_type,
                period=copad.period,
                account_type=copad.account_type,
                base_document=copad.base_document, charge_period=period,
                interest_definition=interestDefinition)
        except AccountCharge.DoesNotExist:
            return None
        
    @classmethod
    def findByCOPADChargePeriodAndPenaltyDefinition(cls, copad, period, penaltyDefinition):
        try:
            return AccountCharge.objects.get(
                client=copad.client,
                concept_type=copad.concept_type,
                period=copad.period,
                account_type=copad.account_type,
                base_document=copad.base_document, charge_period=period,
                penalty_definition=penaltyDefinition)
            
        except AccountCharge.DoesNotExist:
            return None
        
    class Meta:
        app_label = 'accounting'
        db_table = 'acc_account_charge'
        unique_together = ((
            'client',
            'concept_type',
            'period',
            'account_type',
            'charge_period',
            'interest_definition',
            'penalty_definition',
        ),)
        
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
        
