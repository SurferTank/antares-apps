'''
Created on 30/8/2016

@author: leobelen
'''
from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from mptt.fields import TreeForeignKey


class ClientBusinessClassification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_branch = models.ForeignKey(
        "ClientBranch", on_delete=models.PROTECT, db_column='client_branch')
    business_classification = TreeForeignKey(
        "IsicPosition", on_delete=models.PROTECT, db_column='isic_position')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
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
        super(ClientBusinessClassification, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'client'
        db_table = 'cli_client_business_classification'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
