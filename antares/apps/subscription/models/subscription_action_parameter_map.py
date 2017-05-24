'''
Created on Jul 9, 2016

@author: leobelen
'''

import logging
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


class SubscriptionActionParameterMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parameter_definition = models.ForeignKey(
        'core.ActionParameterDefinition',
        on_delete=models.PROTECT,
        related_name='subscription_action_parameter_map_set',
        db_column='parameter_definition',
        blank=True,
        null=True)
    subscription_action = models.ForeignKey(
        'SubscriptionAction',
        on_delete=models.PROTECT,
        db_column='subscription_action',
        related_name='parameter_set',
        blank=True,
        null=True)
    content_text = models.CharField(max_length=255, blank=True, null=True)
    parameter_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(SubscriptionActionParameterMap, self).save(*args, **kwargs)

    class Meta:
        app_label = 'subscription'
        db_table = 'subs_action_parameter_map'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
