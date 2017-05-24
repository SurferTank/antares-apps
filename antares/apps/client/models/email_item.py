import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from enumfields import EnumField
from django.conf import settings

from ..constants import EmailType, ItemStatusType

logger = logging.getLogger(__name__)


class EmailItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_branch = models.ForeignKey(
        "ClientBranch",
        on_delete=models.PROTECT,
        db_column='client_branch',
        blank=True,
        null=True)
    status = EnumField(
        ItemStatusType, max_length=20, default=ItemStatusType.ACTIVE)
    is_principal = models.BooleanField(default=True)
    email_type = EnumField(EmailType, max_length=20)
    email = models.CharField(max_length=256)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(EmailItem, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'client'
        db_table = 'cli_email_item'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
