from antares.apps.core.models import ActionDefinition
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class FormActionMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form_definition = models.ForeignKey(
        "FormDefinition",
        on_delete=models.PROTECT,
        db_column='form_definition',
        blank=True,
        null=True)
    action_definition = models.ForeignKey(
        ActionDefinition,
        on_delete=models.PROTECT,
        db_column='action_definition',
        blank=True,
        null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    action_type = models.CharField(max_length=255)
    active = models.IntegerField(blank=True, null=True)
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField()

    class Meta:
        app_label = 'document'
        db_table = 'doc_action_map'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
