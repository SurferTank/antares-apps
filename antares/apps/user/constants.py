'''
Created on Jul 9, 2016

@author: leobelen
'''
from django.utils.translation import ugettext as _
from enumfields import Enum

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


class UserClassType(EnumUtilsMixin, Enum):
    SCRAPER = "Scraper"
    GENERAL_USER = "General User"
    SPECIALIST = "Specialist"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        SCRAPER = _(__name__ + '.UserClassType.SCRAPER')
        GENERAL_USER = _(__name__ + '.UserClassType.GENERAL_USER')
        SPECIALIST = _(__name__ + '.UserClassType.SPECIALIST')
