import logging
import uuid

from django.db import models
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class FlowActionDefinitionParameterMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action_definition = models.ForeignKey(
        "FlowActionDefinition",
        on_delete=models.PROTECT,
        db_column='action_definition',
        related_name='parameter_set')
    parameter_definition = models.ForeignKey(
        "core.ActionParameterDefinition",
        on_delete=models.PROTECT,
        db_column='action_parameter_definition')
    content = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_action_definition_parameter_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
