'''
Created on Jul 9, 2016

@author: leobelen
'''
import logging
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from antares.apps.core.constants import ScriptEngineType, TimeUnitType
from antares.apps.core.middleware.request import get_request
from enumfields import EnumField
from django.conf import settings

from ..constants import ObligationOriginType, ObligationPeriodicityType, ObligationType

logger = logging.getLogger(__name__)


class ObligationRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form_definition = models.ForeignKey(
        'document.FormDefinition',
        on_delete=models.PROTECT,
        db_column='form_definition',
        blank=True,
        null=True)
    concept_type = models.ForeignKey(
        'core.ConceptType',
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    account_type = models.ForeignKey(
        'accounting.AccountType',
        on_delete=models.PROTECT,
        db_column='account_type',
        blank=True,
        null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)
    active = models.BooleanField(default=True)
    base_date = models.DateTimeField()
    description = RichTextField(blank=True, null=True)
    obligation_condition = models.TextField(blank=True, null=True)
    end_date_expression = models.TextField(blank=True, null=True)
    form_condition = models.TextField(blank=True, null=True)
    init_date_expression = models.TextField(blank=True, null=True)
    last_run = models.DateTimeField(blank=True, null=True, editable=False)
    next_run = models.DateTimeField(blank=True, null=True, editable=False)
    obligation_type = EnumField(ObligationType, max_length=30)
    origin = EnumField(ObligationOriginType, max_length=30)
    periodicity_type = EnumField(ObligationPeriodicityType, max_length=30)
    script_engine_type = EnumField(ScriptEngineType, max_length=30)
    time_unit_type = EnumField(TimeUnitType, max_length=30)
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)
    saturdays_are_holiday = models.BooleanField(default=False)
    sundays_are_holiday = models.BooleanField(default=False)
    consider_holidays = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ObligationRule, self).save(*args, **kwargs)

    @staticmethod
    def find_active_by_concept_type(concept_type):
        try:
            return ObligationRule.objects.filter(
                active=True, concept_type=concept_type)
        except ObligationRule.DoesNotExist:
            return []

    class Meta:
        app_label = 'obligation'
        db_table = 'obl_rule'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
