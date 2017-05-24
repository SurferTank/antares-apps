'''
Created on Jul 25, 2016

@author: leobelen
'''
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from antares.apps.core.middleware.request import get_request
from enumfields import EnumField
from django.conf import settings

from ..constants import ClientRelationPermissionType

logger = logging.getLogger(__name__)


class ClientUserRelationPermission(models.Model):
    '''
    classdocs
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_relation = models.ForeignKey(
        "ClientUserRelation",
        on_delete=models.PROTECT,
        related_name='permission_set',
        db_column='client_user_relation')
    relation_type = EnumField(ClientRelationPermissionType, max_length=20)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="client_user_relation_permission_author_set",
        blank=True,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ClientUserRelationPermission, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'client'
        db_table = 'cli_client_user_relation_permission'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
