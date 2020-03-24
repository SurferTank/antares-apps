from antares.apps.core.constants import ActionParameterDirectionType
from antares.apps.core.constants import FieldDataType
import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class ActionParameterDefinition(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    action_definition = models.ForeignKey(
        "ActionDefinition",
        on_delete=models.PROTECT,
        db_column='action_definition',
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".action_definition"),
        help_text=_(__name__ + ".action_definition_help"))
    data_type = models.TextField(
        choices=FieldDataType.choices,
        max_length=8,
        default=FieldDataType.STRING,
        verbose_name=_(__name__ + ".data_type"),
        help_text=_(__name__ + ".data_type_help"))
    direction = models.TextField(
        choices=ActionParameterDirectionType.choices,
        max_length=6,
        default=ActionParameterDirectionType.IN,
        verbose_name=_(__name__ + ".direction"),
        help_text=_(__name__ + ".direction_help"))
    parameter_name = models.CharField(
        max_length=255,
        verbose_name=_(__name__ + ".parameter_name"),
        help_text=_(__name__ + ".parameter_name_help"))

    def __str__(self):
        return self.action_definition.id + " " + self.parameter_name

    class Meta:
        app_label = 'core'
        db_table = 'core_action_parameter_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
