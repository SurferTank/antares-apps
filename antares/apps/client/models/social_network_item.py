import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from enumfields import EnumField

from antares.apps.core.middleware.request import get_request

from ..constants import SocialNetworkItemType, ItemStatusType


logger = logging.getLogger(__name__)


class SocialNetworkItem(models.Model):
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
    item = models.CharField(max_length=100, blank=True, null=True)
    social_network_type = EnumField(
        SocialNetworkItemType,
        max_length=100,
        default=SocialNetworkItemType.SKYPE)
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
        super(SocialNetworkItem, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'client'
        db_table = 'cli_social_network_item'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
