'''
Created on Jul 9, 2016

@author: leobelen
'''
from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class ObligationOriginType(EnumUtilsMixin, Enum):
    CLIENT_BASE = 'Client Base'
    FORM = 'Form'

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        CLIENT_BASE = _(__name__ + '.ObligationOriginType.' + 'CLIENT_BASE')
        FORM = _(__name__ + '.ObligationOriginType.' + 'FORM')


class ObligationStatusType(EnumUtilsMixin, Enum):
    NOT_EXIGIBLE = "Not Exigible"
    PENDING = "Pending"
    COMPLIANT = "Compliant"
    CANCELLED = "Cancelled"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        NOT_EXIGIBLE = _(__name__ + '.ObligationStatusType.' + 'NOT_EXIGIBLE')
        PENDING = _(__name__ + '.ObligationStatusType.' + 'PENDING')
        COMPLIANT = _(__name__ + '.ObligationStatusType.' + 'PENDING')
        CANCELLED = _(__name__ + '.ObligationStatusType.' + 'CANCELLED')


class ObligationPeriodicityType(EnumUtilsMixin, Enum):
    FIXED_DATE = "Fixed date"
    FIXED_PERIOD = "Fixed period"
    FREE_FORM = "Free form"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        FIXED_DATE = _(__name__ + '.ObligationPeriodicityType.' + 'FIXED_DATE')
        FIXED_PERIOD = _(
            __name__ + '.ObligationPeriodicityType.' + 'FIXED_PERIOD')
        FREE_FORM = _(
            __name__ + '.ObligationPeriodicityType.' + 'FIXED_PERIOD')


class ObligationType(EnumUtilsMixin, Enum):

    # It corresponds with the legal obligation of doing.
    # In this case, it has
    # to be materialized by a document, and hence the obligation is of Filing a
    # document.
    FILE = "File"

    # This is triggered by an special document, the one that has credit effects
    # and works as the unified payment document.
    # For that it relies on a
    # parameterization record stating the code of such document.
    PAY = "Pay"

    # This is utilized to determine that the client has to file a third party
    # delivery remittance, or in other words, has to create a document for each
    # one of the clients he informs and then create a summary with them.
    INFORM = "Inform"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        FILE = _(__name__ + '.ObligationType.' + 'FILE')
        PAY = _(__name__ + '.ObligationType.' + 'PAY')
        INFORM = _(__name__ + '.ObligationType.' + 'INFORM')
