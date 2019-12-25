import logging
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class ReassigmentLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="flow_reassigment_log_signer_set")
    original_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="flow_reassigment_log_original_user_set")
    new_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="flow_reassigment_log_new_user_set")
    flow_case = models.ForeignKey(
        "FlowCase",
        on_delete=models.PROTECT,
        db_column='flow_case',
        related_name="reassigment_set")
    flow_activity = models.ForeignKey(
        "FlowActivity",
        on_delete=models.PROTECT,
        db_column='flow_activity',
        related_name="reassigment_set")
    original_date = models.DateTimeField()
    reason = RichTextField()
    reassigment_date = models.DateTimeField()
    creation_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.author = get_request().user
        super(ReassigmentLog, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_reassignment_log'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
