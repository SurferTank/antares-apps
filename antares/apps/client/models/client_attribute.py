from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class ClientAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(
        "Client",
        on_delete=models.PROTECT,
        db_column='client',
        blank=True,
        null=True)
    attribute_definition = models.ForeignKey(
        "AttributeDefinition",
        on_delete=models.PROTECT,
        db_column='attribute_definition',
        blank=True,
        null=True)
    boolean_value = models.BooleanField(null=True)
    data_type = models.CharField(choices=FieldDataType.choices, max_length=20)
    date_value = models.DateTimeField(blank=True, null=True)
    float_value = models.FloatField(blank=True, null=True)
    integer_value = models.BigIntegerField(blank=True, null=True)
    string_value = models.CharField(max_length=2000, blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ClientAttribute, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'client'
        db_table = 'cli_client_attribute'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
