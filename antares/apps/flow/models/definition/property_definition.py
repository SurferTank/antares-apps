import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

from antares.apps.core.constants import ScriptEngineType
from antares.apps.core.constants import FieldDataType
from enumfields import EnumField
from antares.apps.core.models.system_parameter import SystemParameter

from antares.apps.flow.constants import PropertyType
from antares.apps.flow.constants import FlowDataType
from antares.apps.flow.constants import FormalParameterModeType

logger = logging.getLogger(__name__)


class PropertyDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow_definition = models.ForeignKey(
        "FlowDefinition",
        on_delete=models.PROTECT,
        related_name='property_definition_set',
        db_column='flow_definition',
        blank=True,
        null=True)
    data_type = EnumField(FlowDataType, max_length=30)
    definition_site = models.CharField(max_length=7)
    display_name = models.CharField(max_length=200, blank=True, null=True)
    initial_value = models.CharField(max_length=255, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    property_id = models.CharField(max_length=200)
    property_type = EnumField(PropertyType, max_length=30)
    script_engine = EnumField(ScriptEngineType, max_length=30)
    sub_data_type = EnumField(
        FieldDataType, max_length=30, blank=True, null=True)
    mode = EnumField(
        FormalParameterModeType, max_length=30, blank=True, null=True)
    catalog = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.script_engine is None:
            self.script_engine = ScriptEngineType.to_enum(
                SystemParameter.find_one("DEFAULT_SCRIPT_ENGINE",
                                         FieldDataType.STRING,
                                         str(ScriptEngineType.JAVASCRIPT)))
        super(PropertyDefinition, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def find_one(prop_id):
        try:
            return PropertyDefinition.objects.get(id=prop_id)
        except PropertyDefinition.DoesNotExist:
            return None

    @staticmethod
    def find_by_flow_definition(flow_definition):
        try:
            return PropertyDefinition.objects.filter(
                flow_definition=flow_definition)
        except PropertyDefinition.DoesNotExist:
            return []

    class Meta:
        app_label = 'flow'
        db_table = 'flow_property_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
