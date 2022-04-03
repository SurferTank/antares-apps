'''
Created on Jul 9, 2016

@author: leobelen
'''
import logging
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class SubscriptionAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        'SubscriptionEvent',
        on_delete=models.PROTECT,
        related_name='action_set',
        blank=True,
        null=True)
    action_definition = models.ForeignKey(
        "core.ActionDefinition",
        on_delete=models.PROTECT,
        related_name='subscription_action_set',
        db_column='action_definition')
    order_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(SubscriptionAction, self).save(*args, **kwargs)

    class Meta:
        app_label = 'subscription'
        db_table = 'subs_action'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
