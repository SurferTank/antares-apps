'''
Created on Jul 19, 2016

@author: leobelen
'''

from datetime import datetime
import logging
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey

from antares.apps.core.middleware.request import get_request
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

logger = logging.getLogger(__name__)


class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="role_set")
    role = TreeForeignKey(
        "Role", on_delete=models.PROTECT, related_name="user_set")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(editable=False)
    update_date = models.DateTimeField(editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="user_role_author_set",
        editable=False)

    def save(self, *args, **kwargs):
        from .user import User
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        if (isinstance(get_request().user, AnonymousUser) == False
                and self.author is None):
            self.author = get_request().user
        elif (isinstance(get_request().user, AnonymousUser) == True
              and self.author is None):
            self.author = User.get_system_user()
        super(UserRole, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'user'
        db_table = 'user_user_role'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
