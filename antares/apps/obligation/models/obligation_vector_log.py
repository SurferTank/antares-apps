'''
Created on Jul 9, 2016

@author: leobelen
'''

import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

from ..enums import ObligationStatusType

logger = logging.getLogger(__name__)


class ObligationVectorLog(models.Model):
    """
    Stores the history log for the obligation's vector
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    obligation_status = models.ForeignKey(
        'ObligationVector',
        on_delete=models.PROTECT,
        related_name='obligation_vector_log_set',
        db_column='obligation',
        blank=True,
        null=True)
    status = models.CharField(choices=ObligationStatusType.choices, max_length=30)
    status_date = models.DateTimeField(blank=True, null=True)
    log_date = models.DateTimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='obligation_vector_log_author_set',
        blank=True,
        null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.log_date = timezone.now()
        self.author = get_request().user
        super(ObligationVectorLog, self).save(*args, **kwargs)

    @staticmethod
    def post_status_log(obligation_status):
        status_log = ObligationVectorLog()
        status_log.obligation_status = obligation_status
        status_log.status = obligation_status.status
        status_log.status_date = obligation_status.status_date
        status_log.save()

    class Meta:
        app_label = 'obligation'
        db_table = 'obl_vector_log'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
