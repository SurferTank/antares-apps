import logging
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

logger = logging.getLogger(__name__)


class FlowNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow_case = models.ForeignKey(
        "FlowCase",
        on_delete=models.PROTECT,
        db_column='flow_case',
        related_name='note_set')
    content = RichTextField(blank=True, null=True)
    post_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=2000, blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='author',
        related_name='flow_note_author_set')

    def save(self, *args, **kwargs):
        if self.post_date is None:
            self.post_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(FlowNote, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @classmethod
    def find_one(cls, flow_note_id):
        try:
            return cls.objects.get(id=flow_note_id)
        except cls.DoesNotExist:
            return None

    class Meta:
        app_label = 'flow'
        db_table = 'flow_note'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
