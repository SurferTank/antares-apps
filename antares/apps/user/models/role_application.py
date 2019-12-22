'''
Created on Jul 25, 2016

@author: leobelen
'''
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey

from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class RoleApplication(models.Model):
    '''
    classdocs
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    role = TreeForeignKey(
        "Role", on_delete=models.PROTECT, related_name="application_set")
    application = TreeForeignKey(
        "Application", on_delete=models.PROTECT, related_name="role_set")
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="role_application_author_set",
        editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(RoleApplication, self).save(*args, **kwargs)

    def __str__(self):
        if self.role.name and self.application.application_name:
            return self.role.name + ": " + self.application.application_name
        else:
            return str(self.id)

    class Meta:
        app_label = 'user'
        db_table = 'user_role_application'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
