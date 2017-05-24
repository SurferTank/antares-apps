import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

from enumfields import EnumField

from antares.apps.flow.constants import TransitionType

logger = logging.getLogger(__name__)


class TransitionDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    to_activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        db_column='to_activity_definition',
        blank=True,
        null=True,
        related_name="transition_definition_to_activity_set")
    from_activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        db_column='from_activity_definition',
        blank=True,
        null=True,
        related_name="transition_definition_from_activity_set")
    flow_definition = models.ForeignKey(
        "FlowDefinition",
        on_delete=models.PROTECT,
        related_name='transition_definition_set',
        db_column='flow_definition',
        blank=True,
        null=True)
    condition_text = models.TextField(blank=True, null=True)
    transition_id = models.CharField(max_length=255)
    transition_name = models.CharField(max_length=255, blank=True, null=True)
    transition_type = EnumField(TransitionType, max_length=30)

    def save(self, *args, **kwargs):
        super(TransitionDefinition, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def find_one(doc_id):
        try:
            return TransitionDefinition.objects.get(id=doc_id)
        except TransitionDefinition.DoesNotExist:
            return None

    @staticmethod
    def delete_by_flow_definition(flow_def):
        for transition_def in flow_def.transition_definition_set.select_related(
        ).all():
            transition_def.delete()

    @staticmethod
    def find_incoming_transitions(activity_def):
        try:
            return TransitionDefinition.objects.filter(
                to_activity_definition=activity_def)
        except TransitionDefinition.DoesNotExist:
            return []

    @staticmethod
    def find_outgoing_transitions(activity_def):
        try:
            return TransitionDefinition.objects.filter(
                from_activity_definition=activity_def)
        except TransitionDefinition.DoesNotExist:
            return []

    class Meta:
        app_label = 'flow'
        db_table = 'flow_transition_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
