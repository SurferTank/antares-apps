import logging

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _


from antares.apps.core.middleware.request import get_request

from ..constants import ActionTargetModuleType
from ..constants import EnvironmentType


logger = logging.getLogger(__name__)


class ActionDefinition(models.Model):
    id = models.SlugField(
        max_length=200,
        primary_key=True,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))

    active = models.BooleanField(
        default=True,
        verbose_name=_(__name__ + ".active"),
        help_text=_(__name__ + ".wether_the_row_activated_or_not"))
    definition_content = models.TextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".definition_content"),
        help_text=_(__name__ + ".action_definition_contents"))

    environment = models.TextField(
        choices=EnvironmentType.choices,
        max_length=20,
        default=EnvironmentType.LOCAL,
        verbose_name=_(__name__ + ".environment"),
        help_text=_(__name__ + ".environment_help"))
    executable_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_(__name__ + ".executable_name"),
        help_text=_(__name__ + ".executable_name_help"))
    target_module = models.TextField(
        choices=ActionTargetModuleType.choices,
        max_length=30,
        default=ActionTargetModuleType.DOCUMENT,
        verbose_name=_(__name__ + ".target_module"),
        help_text=_(__name__ + ".target_module_help"))
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
        help_text=_(__name__ + ".author_help"))

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ActionDefinition, self).save(*args, **kwargs)

    def __str__(self):
        if self.executable_name is not None:
            return self.executable_name
        else:
            return str(self.id)

    @staticmethod
    def find_one_or_create_by_params(action_id, **kwargs):
        """
        Returns one action definition and id it does not exists, creates one based on information passed.
        """
        action_def = ActionDefinition.find_one(action_id)
        if (action_def is not None):
            return action_def

        action_def = ActionDefinition()
        action_def.id = action_id
        action_def.creation_date = timezone.now()
        action_def.update_date = timezone.now()
        environment = kwargs.get('environment')

        if (environment is not None):
            action_def.environment = environment

        executable_name = kwargs.get('executable_name')
        if (executable_name):
            action_def.executable_name = executable_name

        target_module = kwargs.get('target_module')
        if (target_module is not None):
            action_def.target_module = target_module

        action_def.save()
        return action_def

    @staticmethod
    def find_one(action_id):
        """
        Returns one action definition and id it does not exists, returns None
        """
        try:
            action_def = ActionDefinition.objects.get(id=action_id)
            return action_def
        except ActionDefinition.DoesNotExist:
            return None

    class Meta:
        app_label = 'core'
        db_table = 'core_action_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
