import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

from ..enums import TelephoneItemType, ItemStatusType

logger = logging.getLogger(__name__)


class TelephoneItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_branch = models.ForeignKey(
        "ClientBranch",
        on_delete=models.PROTECT,
        db_column='client_branch',
        blank=True,
        null=True)
    status = models.CharField(
        max_length=20,
        choices=ItemStatusType.choices,
        default=ItemStatusType.ACTIVE 
    )
    is_principal = models.BooleanField(default=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    telephone_type = models.CharField(
        max_length=20,
        choices=TelephoneItemType.choices,
        default=TelephoneItemType.HOME
    )
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
        super(TelephoneItem, self).save(*args, **kwargs)

    def __str__(self):
        if (self.telephone_type and self.telephone):
            return self.telephone_type + ' ' + self.telephone
        else:
            return str(self.id)

    class Meta:
        app_label = 'client'
        db_table = 'cli_telephone_item'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
