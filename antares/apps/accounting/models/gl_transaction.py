'''
Created on Jun 24, 2016

@author: leobelen
'''
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from djmoney.models.fields import MoneyField
from djmoney.money import Money


logger = logging.getLogger(__name__)


class GLTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(
        "accounting.AccountTransaction",
        on_delete=models.PROTECT,
        db_column='gl_transaction',
        blank=True,
        null=True)
    period = models.IntegerField()
    debit_balance = MoneyField(
        max_digits=15, decimal_places=2, default_currency='USD', default=0, null=False, blank=False, editable=False)
    credit_balance = MoneyField(
        max_digits=15, decimal_places=2, default_currency='USD', default=0, null=False, blank=False, editable=False)
    fiscal_year = models.IntegerField()
    gl_account_type = models.ForeignKey(
        "accounting.GLAccountType",
        on_delete=models.PROTECT,
        db_column='gl_account_type',
        blank=True,
        null=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        super(GLTransaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_gl_transaction'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
