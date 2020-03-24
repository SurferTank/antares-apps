from antares.apps.core.middleware.request import get_request
import logging
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class I18nString(models.Model):
    """
    This class contains the internationalized messages when the input is on the database...
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))

    language = models.CharField(
        max_length=2,
        verbose_name=_(__name__ + ".language_name"),
        help_text=_(__name__ + ".language_name_help"))

    code = models.CharField(
        max_length=100,
        verbose_name=_(__name__ + ".code_name"),
        help_text=_(__name__ + ".code_name_help"))

    is_default = models.BooleanField(
        verbose_name=_(__name__ + ".is_default_name"),
        help_text=_(__name__ + ".is_default_name_help"),
        default=True)

    content = RichTextField(
        verbose_name=_(__name__ + ".content_name"),
        help_text=_(__name__ + ".content_name_help"))

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
        if len(self.language) > 2:
            self.language = self.language[:2]

        self.super(I18nString, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'core'
        db_table = 'core_i18n_string'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
