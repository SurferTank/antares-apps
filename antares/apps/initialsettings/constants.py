'''
Created on Jul 9, 2016

@author: leobelen
'''
from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class SettingsGroupType(EnumUtilsMixin, Enum):
    TAX = 'Tax'
    FINANCIAL = 'Financial'

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        TAX = _(__name__ + '.SettingsGroupType.' + "TAX")
        FINANCIAL = _(__name__ + '.SettingsGroupType.' + "FINANCIAL")
