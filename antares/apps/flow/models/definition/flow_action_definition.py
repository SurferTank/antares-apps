from antares.apps.core.constants import ActionType, ScriptEngineType, FieldDataType
from antares.apps.core.models.system_parameter import SystemParameter
import logging
import uuid

from django.db import models
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class FlowActionDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        db_column='activity_definition',
        related_name='action_definition_set')
    action_definition = models.ForeignKey(
        'core.ActionDefinition',
        on_delete=models.PROTECT,
        db_column='action_definition',
        blank=True,
        null=True)
    action_type = models.CharField(
        choices=ActionType.choices, max_length=30, default=ActionType.POST_ACTION)
    script_engine = models.CharField(choices=ScriptEngineType.choices,
                                     max_length=30)
    content = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def find_by_activity_definition_and_action_type(cls, activity_definition,
                                                    action_type):
        try:
            return cls.objects.filter(
                activity_definition=activity_definition,
                action_type=action_type)
        except cls.DoesNotExist:
            return []

    def save(self, *args, **kwargs):
        if self.script_engine is None:
            self.script_engine = ScriptEngineType.to_enum(
                SystemParameter.find_one("DEFAULT_SCRIPT_ENGINE",
                                         FieldDataType.STRING,
                                         str(ScriptEngineType.JAVASCRIPT)))
        super(FlowActionDefinition, self).save(*args, **kwargs)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_action_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
