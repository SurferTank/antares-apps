import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class AttributeDefinition(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    description = RichTextField(blank=True, null=True)
    display_name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    data_type = models.CharField(choices=FieldDataType.choices, max_length=20)
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
        super(AttributeDefinition, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'client'
        db_table = 'cli_attribute_definition'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
