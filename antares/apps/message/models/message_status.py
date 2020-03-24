'''
Created on Jul 9, 2016

@author: leobelen
'''
from antares.apps.core.constants import SystemModuleType
from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ..constants import MessageStatusType
from ..models.message import Message


logger = logging.getLogger(__name__)


class MessageStatus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    core_object = models.ForeignKey(
        'Message',
        on_delete=models.PROTECT,
        db_column='message',
        related_name="status_set")
    module = models.CharField(choices=SystemModuleType.choices, max_length=30)
    status = models.CharField(choices=MessageStatusType.choices,
                              max_length=30, default=MessageStatusType.PENDING)
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".creation_name"),
        help_text=_(__name__ + ".creation_name_help"))
    update_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".update_date"),
        help_text=_(__name__ + ".update_date_help"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".author"),
        help_text=_(__name__ + ".author_help"))

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(MessageStatus, self).save(*args, **kwargs)

    @classmethod
    def find_or_create_one(cls, **kwargs):
        core_object = Message.find_or_create_one(**kwargs)
        if core_object is None:
            return None
        try:
            status_object = MessageStatus.objects.get(core_object=core_object)
        except MessageStatus.DoesNotExist:
            status_object = MessageStatus()
            if 'module' not in kwargs:
                raise ValueError(
                    _(__name__ + ".exceptions.module_was_not_specified"))
            status_object.core_object = core_object
            status_object.module = kwargs.get('module')
            status_object.save()

        if ('status' in kwargs and MessageStatusType.to_enum(
                status_object.status) != kwargs.get('status')):
            status_object.status = kwargs.get('status')
            status_object.save()
        return status_object

    @classmethod
    def find_one(cls, **kwargs):
        core_object = Message.find_or_create_one(kwargs)
        if core_object is None:
            return None
        status_object = MessageStatus.objects.get(object=core_object)
        if status_object is not None:
            return status_object
        else:
            return None

    def set_status(self, status):
        self.status = str(status)
        self.save()

    class Meta:
        app_label = 'message'
        db_table = 'msg_message_status'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
