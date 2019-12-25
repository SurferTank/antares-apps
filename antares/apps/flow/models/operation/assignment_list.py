import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from enumfields import EnumField

from antares.apps.flow.constants import AssignmentStrategyType


logger = logging.getLogger(__name__)


class AssignmentList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    # organizational_unit = models.ForeignKey('SecOrgUnit', on_delete=models.PROTECT, blank=True, null=True)
    flow_definition = models.ForeignKey(
        "FlowDefinition",
        on_delete=models.PROTECT,
        db_column='flow_definition',
        blank=True,
        null=True)
    flow_case = models.ForeignKey(
        "FlowCase",
        on_delete=models.PROTECT,
        db_column='flow_case',
        blank=True,
        null=True)
    activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        db_column='activity_definition',
        blank=True,
        null=True)
    assigment_strategy = EnumField(AssignmentStrategyType, max_length=30)
    creation_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        super(AssignmentList, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_assignment_list'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
