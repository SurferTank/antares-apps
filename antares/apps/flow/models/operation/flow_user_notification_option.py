from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class FlowUserNotificationOption(models.Model):
    '''
    classdocs
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow_case = models.ForeignKey(
        "FlowCase",
        on_delete=models.PROTECT,
        db_column='flow_case',
        related_name='user_notification_option_set')
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='perfomer',
        related_name='user_notification_option_set')
    active = models.BooleanField(default=False)
    creation_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.performer = get_request().user
        super(FlowUserNotificationOption, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @classmethod
    def find_or_create_one_by_flow_case(cls, flow_case):
        try:
            return cls.objects.get(flow_case=flow_case)
        except cls.DoesNotExist:
            option = FlowUserNotificationOption()
            option.flow_case = flow_case
            option.save()
            return option

    @classmethod
    def find_status_by_flow_case(cls, flow_case):
        try:
            return cls.objects.get(flow_case=flow_case).active
        except cls.DoesNotExist:
            option = FlowUserNotificationOption()
            option.flow_case = flow_case
            option.save()
            return option.active

    class Meta:
        app_label = 'flow'
        db_table = 'flow_user_notification_option'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
