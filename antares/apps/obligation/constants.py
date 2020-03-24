'''
Created on Jul 9, 2016

@author: leobelen
'''
from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class ObligationOriginType(EnumUtilsMixin, models.TextChoices):
    CLIENT_BASE = 'Client Base', _(__name__ + '.ObligationOriginType.' + 'CLIENT_BASE')
    FORM = 'Form', _(__name__ + '.ObligationOriginType.' + 'FORM')


class ObligationStatusType(EnumUtilsMixin, models.TextChoices):
    NOT_EXIGIBLE = "Not Exigible", _(__name__ + '.ObligationStatusType.' + 'NOT_EXIGIBLE')
    PENDING = "Pending", _(__name__ + '.ObligationStatusType.' + 'PENDING')
    COMPLIANT = "Compliant", _(__name__ + '.ObligationStatusType.' + 'COMPLIANT')
    CANCELLED = "Cancelled", _(__name__ + '.ObligationStatusType.' + 'CANCELLED')
    LATE = "Late", _(__name__ + '.ObligationStatusType.' + 'LATE')


class ObligationPeriodicityType(EnumUtilsMixin, models.TextChoices):
    FIXED_DATE = "Fixed date", _(__name__ + '.ObligationPeriodicityType.' + 'FIXED_DATE')
    FIXED_PERIOD = "Fixed period", _(__name__ + '.ObligationPeriodicityType.' + 
                         'FIXED_PERIOD')
    FREE_FORM = "Free form", _(__name__ + '.ObligationPeriodicityType.' + 
                      'FREE_FORM')


class ObligationType(EnumUtilsMixin, models.TextChoices):

    # It corresponds with the legal obligation of doing.
    # In this case, it has
    # to be materialized by a document, and hence the obligation is of Filing a
    # document.
    FILE = "File", _(__name__ + '.ObligationType.' + 'FILE')

    # This is triggered by an special document, the one that has credit effects
    # and works as the unified payment document.
    # For that it relies on a
    # parameterization record stating the code of such document.
    PAY = "Pay", _(__name__ + '.ObligationType.' + 'PAY')

    # This is utilized to determine that the client has to file a third party
    # delivery remittance, or in other words, has to create a document for each
    # one of the clients he informs and then create a summary with them.
    INFORM = "Inform", _(__name__ + '.ObligationType.' + 'INFORM')

