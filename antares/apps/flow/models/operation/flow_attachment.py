import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from antares.apps.core.middleware.request import get_request
from django.conf import settings

logger = logging.getLogger(__name__)


class FlowAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow_case = models.ForeignKey(
        "FlowCase",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="attachment_set")
    content = models.BinaryField()
    file_name = models.CharField(max_length=400)
    mime_type = models.CharField(max_length=100)
    post_date = models.DateTimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='author',
        related_name='flow_attachment_author_set')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.post_date is None:
            self.post_date = timezone.now()
        self.author = get_request().user
        super(FlowAttachment, self).save(*args, **kwargs)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_attachment'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
