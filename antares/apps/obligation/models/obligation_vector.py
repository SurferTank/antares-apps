'''
Created on Jul 9, 2016

@author: leobelen
'''
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

from ..enums import ObligationType, ObligationStatusType,\
        ObligationStatusType

logger = logging.getLogger(__name__)


class ObligationVector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    concept_type = models.ForeignKey(
        'core.ConceptType',
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    source_document = models.ForeignKey(
        'document.DocumentHeader',
        on_delete=models.PROTECT,
        db_column='source_document',
        related_name='obligation_vector_source_document_set',
        blank=True,
        null=True)
    compliance_document = models.ForeignKey(
        'document.DocumentHeader',
        on_delete=models.PROTECT,
        db_column='compliance_document',
        related_name='obligation_vector_compliance_document_set',
        blank=True,
        null=True)
    client_obligation = models.ForeignKey(
        'ClientObligation',
        on_delete=models.PROTECT,
        db_column='client_obligation',
        related_name='obligation_status_client_obligation_set',
        blank=True,
        null=True)
    base_document = models.ForeignKey(
        'document.DocumentHeader',
        on_delete=models.PROTECT,
        related_name='obligation_status_base_document_set',
        db_column='base_document',
        blank=True,
        null=True)
    client = models.ForeignKey(
        'client.Client',
        on_delete=models.PROTECT,
        db_column='client',
        related_name='obligation_status_client_set',
        blank=True,
        null=True)
    account_type = models.ForeignKey(
        'accounting.AccountType',
        on_delete=models.PROTECT,
        related_name='obligation_status_account_type_set',
        db_column='account_type')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='obligation_vector_author_set')
    due_date = models.DateTimeField()
    compliance_date = models.DateTimeField(blank=True, null=True)
    period = models.IntegerField()
    status = models.CharField(choices=ObligationStatusType.choices, max_length=30)
    obligation_type = models.CharField(choices=ObligationType.choices, max_length=30)
    status_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ObligationVector, self).save(*args, **kwargs)

    @classmethod
    def find_or_create_status(cls, client, concept_type, period, account_type,
                              base_document, client_obligation,
                              obligation_type, due_date):
        obligation_status = ObligationVector.find_one_by_COPAD(
            client, concept_type, period, account_type, base_document)
        if (obligation_status is not None):
            return obligation_status
        obligation_status = ObligationVector()
        obligation_status.client = client
        obligation_status.concept_type = concept_type
        obligation_status.period = period
        obligation_status.account_type = account_type
        obligation_status.base_document = base_document
        obligation_status.client_obligation = client_obligation
        obligation_status.status = ObligationStatusType.PENDING
        obligation_status.status_date = timezone.now()
        obligation_status.obligation_type = obligation_type
        obligation_status.due_date = due_date
        obligation_status.save()
        return obligation_status

    @classmethod
    def find_one(cls, obligation_id):
        try:
            return cls.objects.get(id=obligation_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def find_one_by_COPAD(cls, client, concept_type, period, account_type,
                          base_document):
        """
        Looks for an obligation in the obligation's vector by its unique identifiers

        """
        try:
            return ObligationVector.objects.get(
                client=client,
                concept_type=concept_type,
                period=period,
                account_type=account_type,
                base_document=base_document)
        except ObligationVector.DoesNotExist:
            return None

    @classmethod
    def find_by_client(cls, client):
        """
        Looks for the client's obligations

        """
        try:
            return ObligationVector.objects.filter(client=client)
        except ObligationVector.DoesNotExist:
            return []

    @classmethod
    def find_by_client_and_obligation_type(cls, client, obligation_type):
        """
        Looks for the client's obligations

        """
        try:
            return ObligationVector.objects.filter(
                client=client, obligation_type=obligation_type)
        except ObligationVector.DoesNotExist:
            return []

    @classmethod
    def find_by_client_and_obligation_type_and_status(cls, client,
                                                      obligation_type, status):
        """
        Looks for the client's obligations

        """
        try:
            return ObligationVector.objects.filter(
                client=client, obligation_type=obligation_type, status=status)
        except ObligationVector.DoesNotExist:
            return []

    @classmethod
    def find_by_client_and_status(cls, client, status):
        """
        Looks for the client's obligations

        """
        try:
            return ObligationVector.objects.filter(
                client=client, status=status)
        except ObligationVector.DoesNotExist:
            return []

    @classmethod
    def set_obligation_status(cls,
                              obligation_status,
                              status,
                              compliance_document=None):
        """
        Sets an status on the obligation's vector
        """
        obligation_status.status = status
        obligation_status.status_date = timezone.now()
        if (compliance_document is not None):
            obligation_status.compliance_document = compliance_document
        obligation_status.save()

    class Meta:
        app_label = 'obligation'
        db_table = 'obl_vector'
        unique_together = (('client', 'concept_type', 'period', 'account_type',
                            'base_document'), )
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
