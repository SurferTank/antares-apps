import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from .account_balance import AccountBalance
from djmoney.models.fields import MoneyField
from djmoney.money import Money

logger = logging.getLogger(__name__)


class AccountTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.ForeignKey(
        "core.Currency",
        on_delete=models.PROTECT,
        db_column='currency',
        blank=True,
        null=True)
    document = models.ForeignKey(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='document',
        blank=True,
        null=True)
    transaction_type = models.ForeignKey(
        "TransactionType",
        on_delete=models.PROTECT,
        db_column='transaction_type',
        blank=True,
        null=True)
    concept_type = models.ForeignKey(
        "core.ConceptType",
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    client = models.ForeignKey(
        "client.Client",
        on_delete=models.PROTECT,
        db_column='client',
        blank=True,
        null=True)
    account_type = models.ForeignKey(
        "AccountType",
        on_delete=models.PROTECT,
        db_column='account_type',
        blank=True,
        null=True)
    balance = models.ForeignKey(
        "AccountBalance",
        on_delete=models.PROTECT,
        db_column='balance',
        blank=True,
        null=True)
    account_document = models.ForeignKey(
        "AccountDocument",
        on_delete=models.PROTECT,
        db_column='account_document',
        blank=True,
        null=True)
    compliance_date = models.DateTimeField(blank=True, null=True)
    credit_format = models.CharField(max_length=40, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    external_function = models.CharField(
        max_length=1000, blank=True, null=True)
    fiscal_year = models.IntegerField(blank=True, null=True)
    interest_amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=0)
    penalties_amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=0)
    period = models.IntegerField()
    posted_date = models.DateTimeField()
    principal_amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=0)
    total_amount = MoneyField(
        max_digits=10, decimal_places=2, default_currency='USD', default=0)
    transaction_date = models.DateTimeField()
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    hrn_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_(__name__ + ".hrn_code"),
        help_text=_(__name__ + ".hrn_code_help"))

    def save(self, *args, **kwargs):
        from antares.apps.core.models import HrnCode
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.total_amount = self.principal_amount + \
            self.interest_amount + self.penalties_amount
        if not self.hrn_code:
            HrnCode.process_account_balance_hrn_script(self)
        super(AccountTransaction, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    @classmethod
    def find_by_balance(cls, balance: AccountBalance):
        try:
            return cls.objects.filter(balance=balance)
        except cls.DoesNotExist:
            return []

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_transaction'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
