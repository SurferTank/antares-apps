import logging
import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey

from antares.apps.core.constants import LanguageType
from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class IsicPosition(MPTTModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
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
    isic_name = models.CharField(max_length=2000)
    isic_code = models.CharField(max_length=200)
    language = models.CharField(choices=LanguageType.choices, max_length=20)
    description = RichTextField(blank=True, null=True)
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
        super(IsicPosition, self).save(*args, **kwargs)

    def __str__(self):
        return self.isic_code + ' - ' + self.isic_name

    @classmethod
    def find_one(cls, bu_id):
        try:
            return IsicPosition.objects.get(id=bu_id)
        except IsicPosition.DoesNotExist:
            return None

    @classmethod
    def find_one_by_code_and_language(cls, bu_code, language):
        try:
            return IsicPosition.objects.get(
                isic_code=bu_code, language=language)
        except IsicPosition.DoesNotExist:
            return None

    @classmethod
    def save_position(cls, bu_code, bu_name, language):
        if cls.find_one_by_code_and_language(bu_code, language) is None:
            if (not bu_code.isalpha()):
                if (len(bu_code) == 3):
                    parent = cls.find_one_by_code_and_language(
                        bu_code[:-2], language)
                else:
                    parent = cls.find_one_by_code_and_language(
                        bu_code[:-1], language)
            else:
                parent = None

            bu = IsicPosition()
            bu.parent = parent
            bu.isic_code = bu_code
            bu.isic_name = bu_name
            bu.language = language
            bu.save()

    class Meta:
        app_label = 'client'
        db_table = 'cli_isic_position'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
        unique_together = (('isic_code', 'language'), )

    class MPTTMeta:
        order_insertion_by = ['isic_code']
