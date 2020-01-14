'''
Created on Jul 9, 2016

@author: leobelen
'''

from django.utils.translation import ugettext as _
from enumfields import Enum

from antares.apps.core.mixins import EnumUtilsMixin


class EventType(EnumUtilsMixin, Enum):
    CREATION = "Creation"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        CREATION = _('antares.apps.flow.constants.EventType.' + 'CREATION')
