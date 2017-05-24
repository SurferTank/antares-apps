'''
Created on Jul 19, 2016

@author: leobelen
'''
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from enumfields import EnumField
from django.conf import settings

from ..constants import DocumentACLAccessType

logger = logging.getLogger(__name__)


class DocumentACL(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    document = models.ForeignKey(
        "DocumentHeader",
        on_delete=models.PROTECT,
        db_column='form_definition',
        related_name='document_acl_set',
        verbose_name=_(__name__ + ".document"),
        help_text=_(__name__ + ".document_help"))
    org_unit = models.ForeignKey(
        "user.OrgUnit",
        on_delete=models.PROTECT,
        db_column='org_unit',
        verbose_name=_(__name__ + ".org_unit"),
        help_text=_(__name__ + ".org_unit_help"),
        related_name='document_acl_set',
        blank=True,
        null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='user_acl',
        verbose_name=_(__name__ + ".user"),
        help_text=_(__name__ + ".user_help"),
        related_name='document_acl_set',
        blank=True,
        null=True)
    role = models.ForeignKey(
        "user.Role",
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + ".role"),
        related_name="role_acl",
        help_text=_(__name__ + ".role_help"),
        db_column='role',
        blank=True,
        null=True)
    access_type = models.CharField(
        DocumentACLAccessType,
        max_length=30,
        default=DocumentACLAccessType.NONE)
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".creation_name"),
        help_text=_(__name__ + ".creation_name_help"))
    update_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".update_date"),
        help_text=_(__name__ + ".update_date_help"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".author"),
        help_text=_(__name__ + ".author_help"),
        related_name='document_acl_author_set', )

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(DocumentACL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'document'
        db_table = 'doc_document_acl'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
