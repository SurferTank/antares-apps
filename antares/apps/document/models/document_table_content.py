from antares.apps.core.constants import FieldDataType
import logging

from django.db import models
from django.utils.translation import ugettext as _


logger = logging.getLogger(__name__)


class DocumentTableContent(models.Model):
    id = models.BigIntegerField(primary_key=True)
    form_definition = models.ForeignKey(
        "FormDefinition",
        on_delete=models.PROTECT,
        db_column='form_definition',
        blank=True,
        null=True)
    document = models.ForeignKey(
        "DocumentHeader",
        on_delete=models.PROTECT,
        db_column='document',
        blank=True,
        null=True,
        related_name='table_content_set')
    clob_value = models.CharField(max_length=255, blank=True, null=True)
    column_number = models.IntegerField(blank=True, null=True)
    data_type = models.CharField(choices=FieldDataType.choices, max_length=8, blank=True, null=True)
    date_value = models.DateTimeField(blank=True, null=True)
    decimal_value = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True)
    definition = models.CharField(max_length=40, blank=True, null=True)
    integer_value = models.BigIntegerField(blank=True, null=True)
    row_number = models.IntegerField(blank=True, null=True)
    string_value = models.CharField(max_length=2000, blank=True, null=True)
    table_definition = models.CharField(max_length=40, blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'document'
        db_table = 'doc_table_contents'
        unique_together = (('document', 'table_definition', 'row_number',
                            'definition'),)
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
