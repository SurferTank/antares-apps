import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

logger = logging.getLogger(__name__)


class Currency(models.Model):
    id = models.SlugField(
        max_length=10,
        primary_key=True,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    active = models.BooleanField(
        default=True,
        verbose_name=_(__name__ + ".active"),
        help_text=_(__name__ + ".active_help"))
    format = models.CharField(
        max_length=100,
        verbose_name=_(__name__ + ".format"),
        help_text=_(__name__ + ".format_help"))
    short_name = models.CharField(
        max_length=100,
        verbose_name=_(__name__ + ".short_name"),
        help_text=_(__name__ + ".short_name_help"))
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
        super(Currency, self).save(*args, **kwargs)

    def __str__(self):
        return "Currency " + self.id

    class Meta:
        app_label = 'core'
        db_table = 'core_currency'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
