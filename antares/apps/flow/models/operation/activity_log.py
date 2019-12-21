import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

from django.conf import settings

from antares.apps.flow.enums import FlowActivityStatusType

logger = logging.getLogger(__name__)


class ActivityLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='performer',
        related_name="flow_activity_log_performer_set")
    flow_activity = models.ForeignKey(
        "FlowActivity",
        on_delete=models.PROTECT,
        db_column='flow_activity',
        related_name="activity_log_set")
    activity_id = models.CharField(max_length=255)
    contents = models.TextField(blank=True, null=True)
    status =  models.CharField(
        max_length=20,
        choices=FlowActivityStatusType.choices
    ) 
    status_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    @staticmethod
    def find_one(doc_id):
        try:
            return ActivityLog.objects.get(id=doc_id)
        except ActivityLog.DoesNotExist:
            return None

    @staticmethod
    def find_by_flow_activity(flow_activity):
        try:
            return ActivityLog.objects.filter(flow_activity=flow_activity)
        except ActivityLog.DoesNotExist:
            return []

    @staticmethod
    def register_activity_log(activity):
        activityLog = ActivityLog()
        activityLog.flow_activity = activity
        activityLog.activity_id = activity.activity_definition.activity_id
        activityLog.performer = activity.performer
        activityLog.status = activity.status
        activityLog.status_date = activity.status_date
        activityLog.save()

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity_log'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
