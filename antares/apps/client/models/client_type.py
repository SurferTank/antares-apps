import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from enumfields import EnumField

from antares.apps.core.middleware.request import get_request

from ..constants import ClientArchetype


logger = logging.getLogger(__name__)


class ClientType(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    archetype = EnumField(ClientArchetype, max_length=20)
    short_name = models.CharField(max_length=1000)
    description = RichTextField(blank=True, null=True)
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
        super(ClientType, self).save(*args, **kwargs)

    @classmethod
    def find_one(cls, type_id):
        try:
            return cls.objects.get(id=type_id)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'client'
        db_table = 'cli_client_type'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
