import logging
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from antares.apps.core.middleware.request import get_request
from django.conf import settings

logger = logging.getLogger(__name__)


class OrgUnit(MPTTModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE)
    description = RichTextField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True, unique=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="org_unit_author_set",
        blank=True,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(OrgUnit, self).save(*args, **kwargs)

    def __str__(self):
        if self.name is None:
            return str(self.id)
        else:
            return self.name

    @staticmethod
    def find_one_by_code(org_unit_code):
        try:
            return OrgUnit.objects.get(code=org_unit_code)
        except OrgUnit.DoesNotExist:
            return None

    class Meta:
        app_label = 'user'
        db_table = 'user_org_unit'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")

    class MPTTMeta:
        order_insertion_by = ['id']
