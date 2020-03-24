'''
Created on Jul 9, 2016

@author: leobelen
'''
from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class ApplicationScopeType(EnumUtilsMixin, models.TextChoices):
    SELF = "Self", _(__name__ + '.ApplicationScopeType.' + 'SELF')
    NEW_WINDOW = "New Window", _(__name__ + '.ApplicationScopeType.' + 'NEW_WINDOW')
    DIALOG = "Dialog", _(__name__ + '.ApplicationScopeType.' + 'DIALOG')


class UserClassType(EnumUtilsMixin, models.TextChoices):
    SCRAPER = "Scraper", _(__name__ + '.UserClassType.SCRAPER')
    GENERAL_USER = "General User", _(__name__ + '.UserClassType.GENERAL_USER')
    SPECIALIST = "Specialist", _(__name__ + '.UserClassType.SPECIALIST')
