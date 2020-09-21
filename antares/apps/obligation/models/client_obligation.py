'''
Created on Jul 9, 2016

@author: leobelen
'''
from antares.apps.core.manager import COPAD
from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


class ClientObligation(models.Model):
    """
    Contains the information needed to calculate the obligation's status vector
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    obligation_rule = models.ForeignKey(
        'ObligationRule',
        on_delete=models.PROTECT,
        db_column='obligation_rule',
        blank=True,
        null=True)
    concept_type = models.ForeignKey(
        'core.ConceptType',
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    client = models.ForeignKey(
        'client.Client',
        on_delete=models.PROTECT,
        db_column='client',
        blank=True,
        null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column='author')
    account_type = models.ForeignKey(
        'accounting.AccountType',
        on_delete=models.PROTECT,
        db_column='account_type',
        blank=True,
        null=True)
    base_document = models.ForeignKey(
        'document.DocumentHeader',
        on_delete=models.PROTECT,
        related_name='client_obligation_base_document_set',
        db_column='base_obligation',
        blank=True,
        null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField()
    creation_date = models.DateTimeField()
    start_date = models.DateTimeField()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """
        Hooks on the save method to update creation_date, update_date and author
        """
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ClientObligation, self).save(*args, **kwargs)

    @staticmethod
    def find_by_client_and_concept_type(client, concept_type):
        try:
            return ClientObligation.objects.filter(
                client=client, concept_type=concept_type)
        except ClientObligation.DoesNotExist:
            return []
    
    @staticmethod
    def find_all():
        try:
            return ClientObligation.objects
        except ClientObligation.DoesNotExist:
            return []
        
    def get_COPAD(self):
        if(self.base_document is not None):
            return COPAD(client=self.client.id, concept_type=self.concept_type.id,
                     account_type=self.account_type.id, 
                     base_document=self.base_document.id)
        else: 
            return COPAD(client=self.client.id, concept_type=self.concept_type.id,
                     account_type=self.account_type.id)

    @classmethod
    def find_one_by_COPAD(cls, copad):
        """
        Looks for an obligation in the obligation's vector by its unique identifiers

        """
        try:
            return ClientObligation.objects.get(
                client=copad.client,
                concept_type=copad.concept_type,
                account_type=copad.account_type,
                base_document=copad.base_document)
        except ClientObligation.DoesNotExist:
            return None

    class Meta:
        app_label = 'obligation'
        db_table = 'obl_client_obligation'
        unique_together = (('client', 'concept_type'),)
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
