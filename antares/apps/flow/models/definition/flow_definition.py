import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.constants import TimeUnitType
from antares.apps.flow.constants import FlowDefinitionStatusType, FlowPriorityType


logger = logging.getLogger(__name__)


class FlowDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow_package = models.ForeignKey(
        "FlowPackage",
        on_delete=models.PROTECT,
        db_column='flow_package',
        related_name='flow_definition_set',
        blank=True,
        null=True)
    access_level = models.CharField(max_length=7)
    creation_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=200, blank=True, null=True)
    flow_id = models.CharField(max_length=255, blank=True, null=True)
    flow_name = models.CharField(max_length=255, blank=True, null=True)
    flow_version = models.CharField(max_length=255, blank=True, null=True)
    hrn_script = models.CharField(max_length=2000, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=FlowDefinitionStatusType.choices, max_length=30)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    time_unit = models.CharField(choices=TimeUnitType.choices, blank=True, null=True, max_length=30)
    waiting_time = models.FloatField(blank=True, null=True)
    working_time = models.FloatField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    priority = models.CharField(choices=FlowPriorityType.choices, blank=True, null=True, max_length=30)

    def __str__(self):
        if self.display_name:
            return self.display_name
        elif self.flow_name:
            return self.flow_name
        elif self.flow_id and self.flow_version:
            return self.flow_id + '(' + self.flow_version + ')'
        else:
            return str(self.id)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        super(FlowDefinition, self).save(*args, **kwargs)

    @classmethod
    def find_one_by_flow_id_and_flow_version(cls, flow_id, flow_version):
        try:
            return cls.objects.get(flow_id=flow_id, flow_version=flow_version)
        except cls.DoesNotExist:
            return None

    class Meta:
        app_label = 'flow'
        db_table = 'flow_definition'
        unique_together = ['flow_package', 'flow_id', 'flow_version']
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
