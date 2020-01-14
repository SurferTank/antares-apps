'''
Created on Jul 25, 2016

@author: leobelen
'''
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class CurrencyExchangeRate(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    from_currency = models.ForeignKey(
        "Currency",
        on_delete=models.PROTECT,
        related_name='from_currency_exchange_rate_set',
        db_column='from_currency',
        verbose_name=_(__name__ + ".from_currency"),
        help_text=_(__name__ + ".from_currency_help"))
    to_currency = models.ForeignKey(
        "Currency",
        on_delete=models.PROTECT,
        related_name='to_currency_exchange_rate_set',
        db_column='to_currency',
        verbose_name=_(__name__ + ".to_currency"),
        help_text=_(__name__ + ".to_currency_help"))
    rate = models.FloatField(
        verbose_name=_(__name__ + ".rate"),
        help_text=_(__name__ + ".rate_help"))
    start_date = models.DateTimeField(
        verbose_name=_(__name__ + ".start_date"),
        help_text=_(__name__ + ".start_date_help"))
    end_date = models.DateTimeField(
        blank=True,
        verbose_name=_(__name__ + ".end_date"),
        help_text=_(__name__ + ".end_date_help"))
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
        super(CurrencyExchangeRate, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'core'
        db_table = 'core_currency_exchange_rate'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
