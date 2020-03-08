# coding=utf-8

import logging
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request

from ..constants import TransactionAffectedValueType


logger = logging.getLogger(__name__)


class AccountRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_type = models.ForeignKey(
        "TransactionType",
        on_delete=models.PROTECT,
        db_column='transaction_type')
    form_definition = models.ForeignKey(
        "document.FormDefinition",
        on_delete=models.PROTECT,
        db_column='form_definition',
        related_name='account_rule_set')
    concept_type = models.ForeignKey(
        "core.ConceptType",
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    account_type = models.ForeignKey(
        "AccountType",
        on_delete=models.PROTECT,
        db_column='account_type',
        blank=True,
        null=True)
    description = RichTextField(blank=True, null=True)
    account_type_field = models.CharField(
        max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    amount_field = models.CharField(max_length=100)
    client_id_field = models.CharField(max_length=100, blank=True, null=True)
    concept_type_field = models.CharField(
        max_length=100, blank=True, null=True)
    document_field = models.CharField(max_length=100, blank=True, null=True)
    external_function = models.CharField(max_length=100, blank=True, null=True)
    fixed_period = models.IntegerField(blank=True, null=True)
    period_field = models.CharField(max_length=100, blank=True, null=True)
    fixed_client = models.ForeignKey(
        "client.client", blank=True, null=True, on_delete=models.PROTECT)
    value_affected = models.CharField(choices=TransactionAffectedValueType.choices, max_length=20)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(AccountRule, self).save(*args, **kwargs)

    def __str__(self):
        return self.transaction_type.transaction_type_name + ":" + self.form_definition.form_name + ":" \
            + self.amount_field 

    @classmethod
    def find_active_by_form_definition(cls, form_definition):
        try:
            return cls.objects.filter(form_definition=form_definition)
        except cls.DoesNotExist:
            return []

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_account_rule'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
