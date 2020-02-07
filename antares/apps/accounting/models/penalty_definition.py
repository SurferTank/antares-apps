'''
Created on Feb 5, 2020

@author: leobelen
'''
'''
Created on Feb 5, 2020

@author: leobelen
'''
import logging
import uuid


from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext as _
from enumfields import EnumField
from antares.apps.core.constants import TimeUnitType
from antares.apps.core.middleware.request import get_request
from djmoney.models.fields import MoneyField
from djmoney.money import Money

logger = logging.getLogger(__name__)
class PenaltyDefinition(models.Model):
    '''
    classdocs
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, blank=False, null=False)
    description = RichTextField(blank=True, null=True)
    rate = models.FloatField(default=0, null=False, blank=False)
    fixed_rates = MoneyField(
        max_digits=15, decimal_places=2, default_currency='USD', default=0, null=False, blank=False, editable=False)
    periodicity = EnumField(
        TimeUnitType, max_length=10, default=TimeUnitType.MONTH)
    max_rounds = models.BooleanField(null=False, default=False)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(PenaltyDefinition, self).save(*args, **kwargs)
