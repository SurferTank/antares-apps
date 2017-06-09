import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

from enumfields import EnumField

from antares.apps.flow.constants import ActivityType, AssignmentStrategyType,\
    ExecutionModeType, FlowActivityInstantiationType, FlowActivityInstantiationType
from antares.apps.flow.constants import AssignmentStrategyType
from antares.apps.flow.constants import ExecutionModeType
from .transition_definition import TransitionDefinition

logger = logging.getLogger(__name__)


class ActivityDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant_definition_set = models.ManyToManyField(
        "ParticipantDefinition", blank=True)
    flow_definition = models.ForeignKey(
        "FlowDefinition",
        on_delete=models.PROTECT,
        related_name='activity_definition_set',
        db_column='flow_definition',
        blank=True,
        null=True)
    activity_id = models.CharField(max_length=255)
    activity_type = EnumField(ActivityType, max_length=30)
    assignment_strategy = EnumField(
        AssignmentStrategyType, max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    finish_mode = EnumField(ExecutionModeType, max_length=30)
    hrn_script = models.CharField(max_length=2000, blank=True, null=True)
    start_mode = EnumField(ExecutionModeType, max_length=30)
    property_strategy_definition = models.CharField(
        max_length=100, blank=True, null=True)
    activity_strategy_definition = models.CharField(
        max_length=100, blank=True, null=True)
    instantiation = EnumField(
        FlowActivityInstantiationType, blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    waiting_time = models.FloatField(blank=True, null=True)
    working_time = models.FloatField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)

    def __str__(self):
        if self.display_name:
            return self.display_name
        elif self.activity_id:
            return self.activity_id
        else:
            return str(self.id)

    @staticmethod
    def find_one(doc_id):
        try:
            return ActivityDefinition.objects.get(id=doc_id)
        except ActivityDefinition.DoesNotExist:
            return None

    @staticmethod
    def find_by_flow_case(flow_case):
        try:
            return ActivityDefinition.objects.filter(flow_case=flow_case)
        except ActivityDefinition.DoesNotExist:
            return []

    @staticmethod
    def delete_by_flow_case(flow_case):
        for activity_def in flow_case.activity_definition_set.select_related(
        ).all():
            activity_def.delete()

    @staticmethod
    def find_start_activity_definitions(flow_def):
        start_activity_list = []
        for activity_def in flow_def.activity_definition_set.select_related(
        ).all():
            if (len(
                    TransitionDefinition.find_incoming_transitions(
                        activity_def)) == 0):
                start_activity_list.append(activity_def)
        return start_activity_list

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
