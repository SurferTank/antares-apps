import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _


from antares.apps.flow.enums import ActivityApplicationDefinitionScopeType

logger = logging.getLogger(__name__)


class ActivityApplicationDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_definition = models.ForeignKey(
        "ApplicationDefinition",
        on_delete=models.PROTECT,
        related_name='activity_application_definition_set',
        db_column='application_definition',
        blank=True,
        null=True)
    activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        related_name='activity_application_definition_set',
        db_column='activity_definition',
        blank=True,
        null=True)
    scope  = models.CharField(
        max_length=30,
        choices = ActivityApplicationDefinitionScopeType.choices,
        default=ActivityApplicationDefinitionScopeType.SAME)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity_application_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
