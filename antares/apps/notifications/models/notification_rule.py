'''
Created on Jul 9, 2016

@author: leobelen
'''
import logging
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from antares.apps.core.middleware.request import get_request
from antares.apps.document.models.form_definition import FormDefinition
from django.conf import settings

logger = logging.getLogger(__name__)


class NotificationRule(models.Model):
    """
    Contains the information needed to produce new notifications.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_code_variable = models.CharField(
        max_length=200,
        blank=True,
        null=True, )
    date_variable = models.CharField(
        max_length=200,
        blank=True,
        null=True, )
    content_variable = models.CharField(max_length=200, blank=True, null=True)
    content_template = RichTextField(blank=True, null=True)
    title_variable = models.CharField(max_length=200, blank=True, null=True)
    form_definition = models.ForeignKey(
        "document.FormDefinition", related_name='notification_rule_set')
    update_date = models.DateTimeField(editable=False)
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='target_user',
        blank=True,
        null=True,
        related_name="notification_rule_target_user_set")
    target_role = models.ForeignKey(
        "user.Role",
        on_delete=models.PROTECT,
        db_column='target_role',
        blank=True,
        null=True)
    target_unit = models.ForeignKey(
        "user.OrgUnit",
        on_delete=models.PROTECT,
        db_column='target_unit',
        blank=True,
        null=True)
    creation_date = models.DateTimeField(editable=False)
    active = models.BooleanField(default="true")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='author',
        editable=False)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        """
        Hooks on the save method to update creation_date, update_date and author
        """
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(NotificationRule, self).save(*args, **kwargs)

    @classmethod
    def find_by_form_definition(cls, form_definition: FormDefinition):
        try:
            return NotificationRule.objects.filter(
                active=True, form_definition=form_definition)
        except NotificationRule.DoesNotExist:
            return []

    class Meta:
        app_label = 'notifications'
        db_table = 'not_rule'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
