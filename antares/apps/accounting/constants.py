'''
Created on Jun 23, 2016

@author: leobelen
'''
from django.utils.translation import ugettext as _
from django.db import models

from antares.apps.core.mixins import EnumUtilsMixin


class AccountDocumentStatusType(EnumUtilsMixin, models.TextChoices):
    PENDING = "Pending", _(__name__ + '.AccountDocumentStatusType.' + "PENDING")
    PROCESSED = "Processed", _(__name__ + '.AccountDocumentStatusType.' + "PROCESSED")
    WITH_ERRORS = "With Errors", _(__name__ + '.AccountDocumentStatusType.' + "WITH_ERRORS")
    ON_HOLD = "On hold", _(__name__ + '.AccountDocumentStatusType.' + "ON_HOLD")
    CANCELLED = "Cancelled", _(__name__ + '.AccountDocumentStatusType.' + "CANCELLED")


class BalanceStatusType(EnumUtilsMixin, models.TextChoices):
    DEBIT = 'Debit',  _(__name__ + '.BalanceStatusType.' + "DEBIT")
    CREDIT = 'Credit',  _(__name__ + '.BalanceStatusType.' + "CREDIT")
    BALANCED = 'Balanced',  _(__name__ + '.BalanceStatusType.' + "BALANCED")

    
    

class TransactionEffectType(EnumUtilsMixin, models.TextChoices):
    DEBIT = "Debit",  _(__name__ + '.TransactionEffectType.' + "DEBIT")
    CREDIT = "Credit",  _(__name__ + '.TransactionEffectType.' + "CREDIT")


class TransactionAffectedValueType(EnumUtilsMixin, models.TextChoices):
    PRINCIPAL = "Principal",  _(__name__ + '.TransactionAffectedValueType.' +
                      "PRINCIPAL")
    INTEREST = "Interest",  _(__name__ + '.TransactionAffectedValueType.' +
                      "INTEREST")
    PENALTIES = "Penalties",  _(__name__ + '.TransactionAffectedValueType.' +
                      "PENALTIES")
