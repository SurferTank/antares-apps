'''
Created on Jul 9, 2016

@author: leobelen
'''

from django.utils.translation import ugettext as _
from django.db import models

from antares.apps.core.mixins import EnumUtilsMixin


class EventType(EnumUtilsMixin, models.TextChoices):
    CREATION = "Creation", _('antares.apps.flow.constants.EventType.' + 'CREATION')
