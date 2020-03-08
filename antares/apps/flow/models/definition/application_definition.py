import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _


from antares.apps.flow.constants import DefinitionSiteType


logger = logging.getLogger(__name__)


class ApplicationDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    flow_definition = models.ForeignKey(
        "FlowDefinition",
        on_delete=models.PROTECT,
        db_column='flow_definition',
        related_name='application_definition_set',
        blank=True,
        null=True)
    application_id = models.CharField(max_length=100, blank=True, null=True)
    definition_site = models.CharField(choices=DefinitionSiteType.choices, max_length=30)
    description = models.TextField(blank=True, null=True)
    application_name = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    route = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_application_definition'
        unique_together = (('flow_definition', 'application_id'), )
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
