'''
Created on Jul 9, 2016

@author: leobelen
'''

from django.utils.translation import ugettext as _
from django.db import models

class EventType(models.TextChoices):
    CREATION = "Creation", _(__name__ + '.EventType.' + 'CREATION')
