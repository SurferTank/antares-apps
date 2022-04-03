'''
Created on Jun 24, 2016

@author: leobelen
'''

from antares.apps.core.middleware.request import get_request
import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManager  # , TreeForeignKey


logger = logging.getLogger(__name__)


class GLAccountType(MPTTModel):
    id = models.SlugField(primary_key=True, max_length=200)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE)
    account_type_name = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        editable=False,
        on_delete=models.CASCADE)

    objects = TreeManager()

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(GLAccountType, self).save(*args, **kwargs)

    def __str__(self):
        return "GL Account Type " + self.id

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_gl_account_type'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")

    class MPTTMeta:
        order_insertion_by = ['id']
        tree_manager_name = 'objects'
