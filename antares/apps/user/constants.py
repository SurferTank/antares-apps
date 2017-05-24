'''
Created on Jul 9, 2016

@author: leobelen
'''
from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class ApplicationScopeType(EnumUtilsMixin, Enum):
    SELF = "Self"
    NEW_WINDOW = "New Window"
    DIALOG = "Dialog"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        SELF = _(__name__ + '.ApplicationScopeType.' + 'SELF')
        NEW_WINDOW = _(__name__ + '.ApplicationScopeType.' + 'NEW_WINDOW')
        DIALOG = _(__name__ + '.ApplicationScopeType.' + 'DIALOG')
