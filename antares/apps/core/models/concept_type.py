import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey

from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class ConceptType(MPTTModel):
    id = models.SlugField(
        primary_key=True,
        max_length=200,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        verbose_name=_(__name__ + ".parent"),
        help_text=_(__name__ + ".parent_help"),
        on_delete=models.CASCADE)
    concept_type_name = models.CharField(
        max_length=200,
        verbose_name=_(__name__ + ".concept_type_name"),
        help_text=_(__name__ + ".concept_type_name_help"))
    description = RichTextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".description"),
        help_text=_(__name__ + ".description_help"))
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".creation_name"),
        help_text=_(__name__ + ".creation_name_help"))
    update_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".update_date"),
        help_text=_(__name__ + ".update_date_help"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".author"),
        help_text=_(__name__ + ".author_help"))

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ConceptType, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    @staticmethod
    def find_one(conceptTypeId):
        """
        Finds one concept type by id or returns None
        """
        try:
            conceptType = ConceptType.objects.get(id=conceptTypeId)
            return conceptType
        except ConceptType.DoesNotExist:
            return None

    class Meta:
        app_label = 'core'
        db_table = 'core_concept_type'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")

    class MPTTMeta:
        order_insertion_by = ['id']
