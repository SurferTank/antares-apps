'''
Created on Jul 19, 2016

@author: leobelen
'''
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from enumfields import EnumField

from antares.apps.core.middleware.request import get_request

from ..constants import FormDefinitionACLAccessType


logger = logging.getLogger(__name__)


class FormDefinitionACL(models.Model):
    id = models.UUIDField(
        _('antares.apps.document.model.FormDefinitionACL.id'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    form_definition = models.ForeignKey(
        "FormDefinition",
        on_delete=models.PROTECT,
        db_column='form_definition',
        related_name='form_defintion_acl_set')
    org_unit = models.ForeignKey(
        "user.OrgUnit",
        on_delete=models.PROTECT,
        db_column='org_unit',
        related_name='form_defintion_acl_set',
        blank=True,
        null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='user',
        related_name='form_defintion_acl_set',
        blank=True,
        null=True)
    role = models.ForeignKey(
        "user.Role",
        on_delete=models.PROTECT,
        db_column='role',
        related_name='form_defintion_acl_set',
        blank=True,
        null=True)
    access_type = EnumField(
        FormDefinitionACLAccessType,
        max_length=30,
        default=FormDefinitionACLAccessType.NONE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='form_defintion_acl_author_set',
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
        super(FormDefinitionACL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'document'
        db_table = 'doc_form_definition_acl'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
