import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


class PerfHeader(models.Model):
    """
    Contains the header of the performance report
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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
        super(PerfHeader, self).save(*args, **kwargs)

    class Meta:
        app_label = 'performance'
        db_table = 'perf_header'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
