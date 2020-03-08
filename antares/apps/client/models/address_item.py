import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request

from ..constants import AddressType, ItemStatusType


logger = logging.getLogger(__name__)


class AddressItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_branch = models.ForeignKey(
        "ClientBranch",
        on_delete=models.PROTECT,
        db_column='client_branch',
        blank=True,
        null=True)
    address_type = models.CharField(choices=AddressType.choices, max_length=30, default=AddressType.REAL)
    country_code = models.CharField(max_length=2, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=ItemStatusType.choices, max_length=20, default=ItemStatusType.ACTIVE)
    is_principal = models.BooleanField(default=True)
    line_1 = models.CharField(max_length=100, blank=True, null=True)
    line_2 = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

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
        super(AddressItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'client'
        db_table = 'cli_address_item'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
