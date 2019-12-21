import logging
import uuid

from django.db import models
from django.utils.translation import ugettext as _

from django.conf import settings
from antares.apps.flow.enums import ParticipantType

logger = logging.getLogger(__name__)


class ParticipantDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    org_unit = models.ForeignKey(
        'user.OrgUnit',
        on_delete=models.PROTECT,
        related_name='flow_participant_definition_set',
        db_column='org_unit',
        blank=True,
        null=True)
    role = models.ForeignKey(
        'user.Role',
        on_delete=models.PROTECT,
        related_name='flow_participant_definition_set',
        db_column='role',
        blank=True,
        null=True)
    flow_definition = models.ForeignKey(
        "FlowDefinition",
        on_delete=models.PROTECT,
        related_name='participant_definition_set',
        db_column='flow_definition',
        blank=True,
        null=True)
    definition_site = models.CharField(max_length=7)
    participant_id = models.CharField(max_length=255)
    participant_name = models.CharField(max_length=255, blank=True, null=True)
    participant_type =  models.CharField(
        max_length=30,
        choices=ParticipantType.choices
    )
   
    def save(self, *args, **kwargs):
        super(ParticipantDefinition, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'flow'
        db_table = 'flow_participant_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
