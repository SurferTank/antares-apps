import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

from ..constants import DocumentStatusType


logger = logging.getLogger(__name__)


class DocumentHrn(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    document = models.ForeignKey(
        "DocumentHeader",
        on_delete=models.CASCADE,
        verbose_name=_(__name__ + ".document"),
        help_text=_(__name__ + ".document_help"),
        db_column='document',
        related_name="document_hrn_set",
        blank=False,
        null=False)
    hrn_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".hrn_code"),
        help_text=_(__name__ + ".hrn_code_help"))
    hrn_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".hrn_title"),
        help_text=_(__name__ + ".hrn_title_help"))
    status = models.CharField(choices=DocumentStatusType.choices,
        max_length=30,
        default=DocumentStatusType.DRAFTED,
        verbose_name=_(__name__ + ".status"),
        help_text=_(__name__ + ".status_help"))
    until_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".until_date"),
        help_text=_(__name__ + ".until_date_help"))

    class Meta:
        app_label = 'document'
        db_table = 'doc_hrn'
        unique_together = (('document', 'status'), )
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
