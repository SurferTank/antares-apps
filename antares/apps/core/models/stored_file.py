import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class StoredFile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))

    file_name = models.CharField(
        max_length=255,
        verbose_name=_(__name__ + ".file_name"),
        help_text=_(__name__ + ".file_name_help"))
    mime_type = models.CharField(
        max_length=50,
        verbose_name=_(__name__ + ".mime_type"),
        help_text=_(__name__ + ".mime_type_help"))
    file_content = models.BinaryField(
        verbose_name=_(__name__ + ".file_content"),
        help_text=_(__name__ + ".file_content_help"))
    alternate_text = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".alternate_text"),
        help_text=_(__name__ + ".alternate_text_help"))
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

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(StoredFile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'core'
        db_table = 'core_stored_file'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
