import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey

from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class UserOrgUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="org_unit_set",
        blank=True,
        null=True)
    org_unit = TreeForeignKey(
        "OrgUnit",
        on_delete=models.PROTECT,
        related_name="user_set",
        blank=True,
        null=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="user_org_unit_author_set",
        editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(UserOrgUnit, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'user'
        db_table = 'user_user_org_unit'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
