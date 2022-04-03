import logging
import uuid

from django.db import models
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class FlowActivityExtraTab(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity_definition = models.ForeignKey(
        "ActivityDefinition",
        on_delete=models.PROTECT,
        db_column='activity_definition',
        related_name='extra_tab_set')
    tab_name = models.CharField(max_length=2000, blank=True, null=True)
    tab_id = models.CharField(max_length=200)
    route = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_activity_extra_tab'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
