'''
Created on Jul 9, 2016

@author: leobelen
'''
from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class SettingsGroupType(EnumUtilsMixin, models.TextChoices):
    TAX = 'Tax', _(__name__ + '.SettingsGroupType.' + "TAX")
    FINANCIAL = 'Financial', _(__name__ + '.SettingsGroupType.' + "FINANCIAL")
