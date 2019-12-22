'''
Created on Jul 19, 2016

@author: leobelen
'''
import logging
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from antares.apps.core.middleware.request import get_request

from .user import User


logger = logging.getLogger(__name__)


class Role(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="role_author_set",
        blank=True,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        if (isinstance(get_request().user, AnonymousUser) == False
                and self.author is None):
            self.author = get_request().user
        elif (isinstance(get_request().user, AnonymousUser) == True
              and self.author is None):
            self.author = User.get_system_user()
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        if self.name is None:
            return str(self.id)
        else:
            return self.name

    @staticmethod
    def find_one_by_code(role_code):
        try:
            return Role.objects.get(code=role_code)
        except Role.DoesNotExist:
            return None

    class Meta:
        app_label = 'user'
        db_table = 'user_role'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")

    class MPTTMeta:
        order_insertion_by = ['id']
