import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class FlowActivityForm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        db_column='activity_definition',
        related_name='form_set')
    form_definition = models.ForeignKey(
        "document.FormDefinition",
        on_delete=models.PROTECT,
        db_column='form_definition',
        related_name='flow_activity_form_set')
    can_save = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity_form'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
