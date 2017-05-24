import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

from antares.apps.core.constants import ScriptEngineType
from enumfields import EnumField

logger = logging.getLogger(__name__)


class FlowActivityValidation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        db_column='activity_definition',
        related_name='validation_set')
    validation_id = models.CharField(max_length=2000)
    validation = models.CharField(max_length=2000)
    message = models.CharField(max_length=2000)
    script_type = EnumField(
        ScriptEngineType, max_length=30, default=ScriptEngineType.JAVASCRIPT)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity_validation'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
