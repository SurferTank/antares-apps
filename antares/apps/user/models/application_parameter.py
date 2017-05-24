import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


class ApplicationParameter(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    application = models.ForeignKey(
        "Application",
        on_delete=models.PROTECT,
        db_column='action_definition',
        related_name='parameter_set',
        verbose_name=_(__name__ + ".action_definition"),
        help_text=_(__name__ + ".action_definition_help"))
    parameter_name = models.CharField(
        max_length=255,
        verbose_name=_(__name__ + ".parameter_name"),
        help_text=_(__name__ + ".parameter_name_help"))
    value = models.CharField(
        max_length=200,
        verbose_name=_(__name__ + ".value_type"),
        help_text=_(__name__ + ".value_help"))
    is_route_parameter = models.BooleanField(
        default=False,
        verbose_name=_(__name__ + ".is_route_parameter"),
        help_text=_(__name__ + ".is_route_parameter_help"))
    is_named_route_parameter = models.BooleanField(
        default=False,
        verbose_name=_(__name__ + ".is_named_route_parameter"),
        help_text=_(__name__ + ".is_named_route_parameter_help"))

    def __str__(self):
        return self.application.application_name + " " + self.parameter_name

    class Meta:
        app_label = 'user'
        db_table = 'user_application_parameter'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
