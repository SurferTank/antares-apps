'''
Created on 30/8/2016

@author: leobelen
'''
from antares.apps.core.middleware.request import get_request
import logging
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class ClientBranch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        "Client",
        on_delete=models.PROTECT,
        db_column='client',
        related_name='branch_set')
    branch_name = models.CharField(max_length=200)
    branch_number = models.IntegerField(default=0)
    description = RichTextField(blank=True, null=True)
    registration_date = models.DateTimeField()
    occupation_description = RichTextField(blank=True, null=True)
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
        if (get_request() is not None
                and isinstance(get_request().user, AnonymousUser) == False
                and self.author is None):
            self.author = get_request().user
        elif (get_request() is None
              or isinstance(get_request().user, AnonymousUser) == True):
            self.author = self.client.user
        super(ClientBranch, self).save(*args, **kwargs)

    def __str__(self):
        return self.client.code + '-' + str(
            self.branch_number) + ' - ' + self.branch_name

    @classmethod
    def find_one_by_client_and_branch_number(cls, client, branch_number=0):
        try:
            return cls.objects.get(client=client, branch_number=branch_number)
        except cls.DoesNotExist:
            return None

    @classmethod
    def find_one(cls, client_branch_id):
        try:
            return cls.objects.get(id=client_branch_id)
        except cls.DoesNotExist:
            return None

    class Meta:
        app_label = 'client'
        db_table = 'cli_client_branch'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
        unique_together = ['client', 'branch_number']
