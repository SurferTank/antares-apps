import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _
from enumfields import EnumField

from antares.apps.core.constants import FieldDataType
from antares.apps.flow.constants import DefinitionSiteType, FlowDataType, PropertyType


logger = logging.getLogger(__name__)


class ApplicationParameterDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_definition = models.ForeignKey(
        "ApplicationDefinition",
        on_delete=models.PROTECT,
        related_name='parameter_definition_set',
        db_column='application_definition',
        blank=True,
        null=True)
    data_type = EnumField(FlowDataType, max_length=30)
    definition_site = EnumField(DefinitionSiteType, max_length=30)
    display_name = models.CharField(max_length=200, blank=True, null=True)
    initial_value = models.CharField(max_length=255, blank=True, null=True)
    length = models.IntegerField(blank=True, null=True)
    order_number = models.IntegerField(blank=True, null=True)
    parameter_id = models.CharField(max_length=200)
    property_type = EnumField(PropertyType, max_length=30)
    sub_data_type = EnumField(
        FieldDataType, max_length=30, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_application_parameter_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
