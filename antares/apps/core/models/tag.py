from antares.apps.core.middleware.request import get_request
import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class Tag(models.Model):
    id = models.SlugField(
        primary_key=True,
        max_length=255,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".description"),
        help_text=_(__name__ + ".description_help"))
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
        if get_request() is not None:
            self.author = get_request().user
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'core'
        db_table = 'core_tag'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
