'''
Created on Jul 9, 2016

@author: leobelen
'''
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..constants import NotificationStatusType


logger = logging.getLogger(__name__)


class NotificationRecord(models.Model):
    """
    Contains the information needed to calculate the obligation's status vector
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post_date = models.DateTimeField()
    content = models.CharField(max_length=2000)
    title = models.CharField(max_length=2000)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='recipient',
        blank=True,
        null=True,
        related_name="notification_recipient_set")
    flow_case = models.ForeignKey(
        "flow.FlowCase",
        on_delete=models.PROTECT,
        db_column='flow_case',
        blank=True,
        null=True)
    document = models.ForeignKey(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='document_header',
        blank=True,
        null=True)
    status = models.CharField(choices=NotificationStatusType.choices,
                              max_length=30,
                              default=NotificationStatusType.POSTED)
    update_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='author',
        blank=True,
        null=True)
    post_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """
        Hooks on the save method to update creation_date, update_date and author
        """
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        super(NotificationRecord, self).save(*args, **kwargs)

    class Meta:
        app_label = 'notifications'
        db_table = 'not_record'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
