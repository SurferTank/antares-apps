import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class FlowActivityExtraTabParameter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tab = models.ForeignKey(
        "FlowActivityExtraTab",
        on_delete=models.PROTECT,
        db_column='tab',
        related_name='parameter_set')
    param_id = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity_extra_tab_parameter'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
