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
from django.db.models import Q

logger = logging.getLogger(__name__)
class InterestDefinition(models.Model):
    '''
    classdocs
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100, blank=False, null=False, unique=True)
    description = RichTextField(blank=True, null=True)
    rate = models.FloatField(null=False, blank=False)
    periodicity = EnumField(
        TimeUnitType, max_length=10, default=TimeUnitType.MONTH)
    first_is_duedate = models.BooleanField(null=False, default=False)
    use_calendar_periods = models.BooleanField(null=False, default=False)
    concept_type = models.ForeignKey(
        "core.ConceptType",
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    active = models.BooleanField(default=True)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def findAllAndByConceptType(cls, conceptType):
        try:
            return cls.filter(Q(concept_type__isNull=True) | Q(concept_type=conceptType) )
        except cls.DoesNotExist:
            return []
    
    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(InterestDefinition, self).save(*args, **kwargs)

        