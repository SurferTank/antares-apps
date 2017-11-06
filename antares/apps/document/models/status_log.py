import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _
from enumfields import EnumField
from ..constants import DocumentStatusType

logger = logging.getLogger(__name__)


class StatusLog(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    status = EnumField(
        DocumentStatusType,
        max_length=30,
        verbose_name=_(__name__ + ".status"),
        help_text=_(__name__ + ".status_help"))
    status_date = models.DateTimeField(
        verbose_name=_(__name__ + ".status_date"),
        help_text=_(__name__ + ".status_date_help"))
    user_id = models.UUIDField(
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".user_id_help"),
        null=True,
        blank=True)
    document_id = models.UUIDField(
        verbose_name=_(__name__ + ".document_id"),
        help_text=_(__name__ + ".document_id_help"),
    )

    class Meta:
        app_label = 'document'
        db_table = 'doc_status_log'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
