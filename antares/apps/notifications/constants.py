'''
Created on Jul 9, 2016

@author: leobelen
'''
from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class NotificationStatusType(EnumUtilsMixin, Enum):
    VIEWED = 'Viewed'
    POSTED = 'Posted'

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        VIEWED = _(__name__ + '.NotificationStatusType.' + 'VIEWED')
        POSTED = _(__name__ + '.NotificationStatusType.' + 'POSTED')


class NotificationDocumentStatusType(EnumUtilsMixin, Enum):
    PENDING = "Pending"
    PROCESSED = "Processed"
    WITH_ERRORS = "With Errors"
    ON_HOLD = "On Hold"
    CANCELLED = "Cancelled"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        PENDING = _(__name__ + '.NotificationDocumentStatusType.' + 'PENDING')
        PROCESSED = _(__name__ + '.NotificationDocumentStatusType.' +
                      'PROCESSED')
        WITH_ERRORS = _(__name__ + '.NotificationDocumentStatusType.' +
                        'WITH_ERRORS')
        ON_HOLD = _(__name__ + '.NotificationDocumentStatusType.' + 'ON_HOLD')
        CANCELLED = _(__name__ + '.NotificationDocumentStatusType.' +
                      'CANCELLED')
