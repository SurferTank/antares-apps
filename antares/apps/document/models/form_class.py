from antares.apps.core.middleware.request import get_request
import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from ..constants import FormClassStatusType, FormClassType


logger = logging.getLogger(__name__)


class FormClass(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    third_party_summary_type = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        db_column='third_party_summary_type',
        blank=True,
        null=True)
    concept_type = models.ForeignKey(
        "core.ConceptType",
        on_delete=models.PROTECT,
        db_column='concept_type',
        blank=True,
        null=True)
    account_type = models.ForeignKey(
        "accounting.AccountType",
        on_delete=models.PROTECT,
        db_column='account_type',
        blank=True,
        null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)
    type = models.CharField(choices=FormClassType.choices, max_length=30, default=FormClassType.ADMINISTRATIVE)
    description = RichTextField(blank=True, null=True)
    status = models.CharField(choices=FormClassStatusType.choices,
        max_length=30,
        default=FormClassStatusType.DEVELOPMENT)
    third_party_type = models.CharField(
        max_length=200, db_index=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        if get_request() is not None:
            self.author = get_request().user
        super(FormClass, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @classmethod
    def find_one_by_third_party_type(cls, third_party_type):
        try:
            return cls.objects.get(third_party_type=third_party_type)
        except cls.DoesNotExist:
            return None

    class Meta:
        app_label = 'document'
        db_table = 'doc_form_class'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
