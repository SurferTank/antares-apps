import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from enumfields import EnumField

from ..constants import AccountDocumentStatusType

logger = logging.getLogger(__name__)


class AccountDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.OneToOneField(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='document_header')
    content = models.TextField(blank=True, null=True)
    reversed_by = models.TextField(blank=True, null=True)
    reverses_document = models.TextField(blank=True, null=True)
    status = EnumField(AccountDocumentStatusType, max_length=30)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        super(AccountDocument, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def find_or_create_by_document(document_header):
        document = AccountDocument._find_one_by_document_header(
            document_header)
        if (document is None):
            document = AccountDocument()
            document.document = document_header
            document.status = str(AccountDocumentStatusType.PENDING)
            document.save()
        return document

    @staticmethod
    def _find_one_by_document_header(document):
        try:
            return AccountDocument.objects.get(document=document)
        except AccountDocument.DoesNotExist:
            return None

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_account_document'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
