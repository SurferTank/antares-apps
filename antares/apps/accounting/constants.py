'''
Created on Jun 23, 2016

@author: leobelen
'''
from django.utils.translation import ugettext as _
from enumfields import Enum

from antares.apps.core.mixins import EnumUtilsMixin


class AccountDocumentStatusType(EnumUtilsMixin, Enum):
    PENDING = "Pending"
    PROCESSED = "Processed"
    WITH_ERRORS = "With Errors"
    ON_HOLD = "On hold"
    CANCELLED = "Cancelled"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        PENDING = _(__name__ + '.AccountDocumentStatusType.' + "PENDING")
        PROCESSED = _(__name__ + '.AccountDocumentStatusType.' + "PROCESSED")
        WITH_ERRORS = _(__name__ + '.AccountDocumentStatusType.' +
                        "WITH_ERRORS")
        ON_HOLD = _(__name__ + '.AccountDocumentStatusType.' + "ON_HOLD")
        CANCELLED = _(__name__ + '.AccountDocumentStatusType.' + "CANCELLED")


class BalanceStatusType(EnumUtilsMixin, Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"
    BALANCED = "Balanced"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        DEBIT = _(__name__ + '.BalanceStatusType.' + "DEBIT")
        CREDIT = _(__name__ + '.BalanceStatusType.' + "CREDIT")
        BALANCED = _(__name__ + '.BalanceStatusType.' + "BALANCED")


class TransactionEffectType(EnumUtilsMixin, Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        DEBIT = _(__name__ + '.TransactionEffectType.' + "DEBIT")
        CREDIT = _(__name__ + '.TransactionEffectType.' + "CREDIT")


class TransactionAffectedValueType(EnumUtilsMixin, Enum):
    PRINCIPAL = "Principal"
    INTEREST = "Interest"
    PENALTIES = "Penalties"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        PRINCIPAL = _(__name__ + '.TransactionAffectedValueType.' +
                      "PRINCIPAL")
        INTEREST = _(__name__ + '.TransactionAffectedValueType.' + "INTEREST")
        PENALTIES = _(__name__ + '.TransactionAffectedValueType.' +
                      "PENALTIES")
