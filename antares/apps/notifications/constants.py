'''
Created on Jul 9, 2016

@author: leobelen
'''
from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class NotificationStatusType(EnumUtilsMixin, models.TextChoices):
    VIEWED = 'Viewed', _(__name__ + '.NotificationStatusType.' + 'VIEWED')
    POSTED = 'Posted', _(__name__ + '.NotificationStatusType.' + 'POSTED')


class NotificationDocumentStatusType(EnumUtilsMixin, models.TextChoices):
    PENDING = "Pending", _(__name__ + '.NotificationDocumentStatusType.' + 'PENDING')
    PROCESSED = "Processed", _(__name__ + '.NotificationDocumentStatusType.' + 
                      'PROCESSED')
    WITH_ERRORS = "With Errors", _(__name__ + '.NotificationDocumentStatusType.' + 
                        'WITH_ERRORS')
    ON_HOLD = "On Hold", _(__name__ + '.NotificationDocumentStatusType.' + 'ON_HOLD')
    CANCELLED = "Cancelled", _(__name__ + '.NotificationDocumentStatusType.' + 
                      'CANCELLED')
    
