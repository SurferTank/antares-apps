'''
Created on Jul 9, 2016

@author: leobelen
'''

from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import gettext as _


class EventType(EnumUtilsMixin, models.TextChoices):
    CREATION = "Creation", _(
        'antares.apps.flow.constants.EventType.' + 'CREATION')
