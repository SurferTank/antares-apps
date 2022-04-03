from antares.apps.core.constants import FieldDataType
import logging
import uuid

from django.db import models
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class DocumentField(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    form_definition = models.ForeignKey(
        "FormDefinition",
        on_delete=models.CASCADE,
        verbose_name=_(__name__ + ".form_definition"),
        help_text=_(__name__ + ".form_definition_help"),
        related_name='field_set',
        db_column='form_definition')
    document = models.ForeignKey(
        "DocumentHeader",
        on_delete=models.CASCADE,
        verbose_name=_(__name__ + ".document"),
        help_text=_(__name__ + ".document_help"),
        related_name='field_set',
        db_column='document')
    clob_value = models.BinaryField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".clob_value"),
        help_text=_(__name__ + ".clob_value_help"))
    data_type = models.CharField(choices=FieldDataType.choices,
                                 max_length=30,
                                 verbose_name=_(__name__ + ".data_type"),
                                 help_text=_(__name__ + ".data_type_help"))
    date_value = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".date_value"),
        help_text=_(__name__ + ".date_value_help"))
    float_value = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".float_value"),
        help_text=_(__name__ + ".float_value_help"))
    definition = models.CharField(
        max_length=40,
        verbose_name=_(__name__ + ".definition"),
        help_text=_(__name__ + ".definition_help"))
    integer_value = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".integer_value"),
        help_text=_(__name__ + ".integer_value_help"))
    ordinal = models.IntegerField(
        default=0,
        verbose_name=_(__name__ + ".ordinal"),
        help_text=_(__name__ + ".ordinal_help"))
    string_value = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".string_value"),
        help_text=_(__name__ + ".string_value_help"))
    text_value = models.TextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".text_value"),
        help_text=_(__name__ + ".text_value_help"))
    uuid_value = models.UUIDField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".uuid_value"),
        help_text=_(__name__ + ".uuid_value_help"))
    comments = models.TextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".comments_value"),
        help_text=_(__name__ + ".comments_help"))

    @classmethod
    def find_one(cls, document_header, definition):
        try:
            field_list = cls.objects.filter(
                document=document_header, definition=definition)
            if field_list.count() > 0:
                return field_list[0]
            else:
                return None
        except cls.DoesNotExist:
            return None

    class Meta:
        app_label = 'document'
        db_table = 'doc_field'
        unique_together = (('definition', 'document'),)
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
