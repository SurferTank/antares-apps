import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

from ..enums import ItemStatusType

logger = logging.getLogger(__name__)


class IdentificationItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        "Client", on_delete=models.PROTECT, db_column='client')
    code = models.CharField(max_length=100)
    type = models.ForeignKey(
        "ClientIdentificationType", on_delete=models.PROTECT, db_column='type')
    status = models.CharField(
        max_length=20,
        choices=ItemStatusType.choices,
        default=ItemStatusType.ACTIVE 
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, editable=False)
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(IdentificationItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.client.code + ' - ' + self.type.id + ' - ' + self.code

    class Meta:
        app_label = 'client'
        db_table = 'cli_identification_item'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
