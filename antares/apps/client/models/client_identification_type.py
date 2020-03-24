from antares.apps.core.middleware.request import get_request
import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class ClientIdentificationType(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    display_name = models.CharField(max_length=100)
    description = RichTextField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False)
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ClientIdentificationType, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'client'
        db_table = 'cli_identification_type'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
