import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


class ActivityApplicationParameterDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_parameter_definition = models.ForeignKey(
        "ApplicationParameterDefinition",
        on_delete=models.PROTECT,
        related_name='parameter_definition_set',
        db_column='application_parameter_definition',
        blank=True,
        null=True)
    activity_application = models.ForeignKey(
        "ActivityApplicationDefinition",
        on_delete=models.PROTECT,
        related_name='parameter_definition_set',
        db_column='activity_application',
        blank=True,
        null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity_application_parameter_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
