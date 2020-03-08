'''
Created on Jul 9, 2016

@author: leobelen
'''
from django.utils.translation import ugettext as _
from django.db import models

from antares.apps.core.mixins import EnumUtilsMixin


class SettingsGroupType(EnumUtilsMixin, models.TextChoices):
    TAX = 'Tax', _(__name__ + '.SettingsGroupType.' + "TAX")
    FINANCIAL = 'Financial',  _(__name__ + '.SettingsGroupType.' + "FINANCIAL")
