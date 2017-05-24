import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from ..constants import BalanceStatusType
from enumfields import EnumField

logger = logging.getLogger(__name__)


class AccountBalance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    default_currency = models.ForeignKey(
        "core.Currency",
        on_delete=models.PROTECT,
        db_column='default_currency',
        blank=True,
        null=True)
    concept_type = models.ForeignKey(
        "core.ConceptType",
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    compliance_document = models.ForeignKey(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='compliance_document',
        blank=True,
        null=True,
        related_name="account_document_compliance_document_set")
    base_document = models.ForeignKey(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='base_document',
        blank=True,
        null=True,
        related_name="account_document_base_document_set")
    client = models.ForeignKey(
        "client.Client", on_delete=models.PROTECT, db_column='client')
    account_type = models.ForeignKey(
        "AccountType", on_delete=models.PROTECT, db_column='account_type')

    balance_status = EnumField(
        BalanceStatusType, max_length=10, default=BalanceStatusType.BALANCED)

    calculation_date = models.DateTimeField()
    compliance_date = models.DateTimeField(blank=True, null=True)
    interest_balance = models.DecimalField(
        max_digits=19, decimal_places=2, default=0)
    penalties_balance = models.DecimalField(
        max_digits=19, decimal_places=2, default=0)
    period = models.IntegerField()
    principal_balance = models.DecimalField(
        max_digits=19, decimal_places=2, default=0)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    total_balance = models.DecimalField(
        max_digits=19, decimal_places=2, default=0)
    hrn_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_(__name__ + ".hrn_code"),
        help_text=_(__name__ + ".hrn_code_help"))

    def save(self, *args, **kwargs):
        from antares.apps.core.models import HrnCode
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.total_balance = self.principal_balance + \
            self.interest_balance + self.penalties_balance
        if not self.hrn_code:
            HrnCode.process_account_balance_hrn_script(self)
        super(AccountBalance, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def find_or_create_by_CCPAD(client, concept_type, period, account_type,
                                document):
        """
        Returns the account balance that matches the unique identifiers - COPAD
        (Client, Concept type, Period, Account type and Document). If none is
        found, it creates one balance with zeroes.
        """
        balance = AccountBalance.find_by_CCPAD(client, concept_type, period,
                                               account_type, document)
        if (balance is not None):
            return balance
        else:
            balance = AccountBalance()
            balance.account_type = account_type
            balance.client = client
            balance.status = str(BalanceStatusType)
            balance.principal_balance = 0
            balance.interest_balance = 0
            balance.penalties_balance = 0
            balance.calculation_date = timezone.now()
            balance.creation_date = timezone.now()
            if (concept_type is not None):
                balance.concept_type = concept_type
            balance.period = period
            if (document is not None):
                balance.document = document
            balance.save()
            return balance

    @staticmethod
    def find_by_CCPAD(client, concept_type, period, account_type, document):
        """
        Gets a balance by Client, concept type, Period, Account Type or, if a document based document, by
            Client, Document, Period, Account type. It infers the document based account based on the document being not none.
        """
        try:
            if (document is None):
                balance_list = list(
                    AccountBalance.objects.filter(
                        client=client,
                        concept_type=concept_type,
                        period=period,
                        account_type=account_type))
                if (len(balance_list) > 0):
                    return balance_list[0]
                else:
                    return None
            else:
                balance_list = list(
                    AccountBalance.objects.filter(
                        client=client,
                        document=document,
                        period=period,
                        account_type=account_type))
                if (len(balance_list) > 0):
                    return balance_list[0]
                else:
                    return None

        except AccountBalance.DoesNotExist:
            return None

    @classmethod
    def get_total_balance_by_client(cls, client):
        from antares.apps.client.models import Client
        if (client is None or client == ""):
            logger.info("The client is empty")
            return 0
        if isinstance(client, str):
            client = Client.find_one(uuid.UUID(client))
            if client is None:
                logger.info("The client was not found")
                return 0
        elif isinstance(client, uuid.UUID):
            client = Client.find_one(client)
            if (client is None):
                logger.info("The client was not found")
                return 0
        result = cls.objects.filter(client=client).exclude(
            account_type__exigible=False).aggregate(
                total_balance=models.Sum(models.F('total_balance')))
        return result['total_balance']

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_account_balance'
        #unique_together = (('client', 'concept_type', 'period', 'account_type',
        #                    'base_document', ), )
        unique_together = (('client', 'concept_type', 'period',
                            'account_type', ), )
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
