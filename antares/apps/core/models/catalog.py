from antares.apps.core.middleware.request import get_request
import ast
import logging

from django.conf import settings
from django.db import connection
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class Catalog(models.Model):
    id = models.SlugField(
        primary_key=True,
        max_length=200,
        verbose_name=_(__name__ + ".id"))
    document_header = models.ForeignKey(
        "document.DocumentHeader",
        on_delete=models.PROTECT,
        db_column='document_header',
        blank=True,
        null=True,
        editable=False,
        verbose_name=_(__name__ + ".document_header"))

    content = models.TextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".content"))
    sql_text = models.CharField(
        max_length=3000,
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".sql_text"))
    creation_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".creation_name"))
    update_date = models.DateTimeField(
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".update_date"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        editable=False,
        verbose_name=_(__name__ + ".author"))

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(Catalog, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    @classmethod
    def find_dict_by_catalog_id(cls, catalog_id: str, query=None) -> {}:
        try:
            catalog_def = Catalog.objects.get(pk=catalog_id)
        except Catalog.DoesNotExist:
            raise ValueError(__name__ + ".exceptions.catalog_was_not_found")
        if (catalog_def.content):
            result = ast.literal_eval(catalog_def.content)
        elif (catalog_def.sql_text):
            # we have to execute a SQL to get it.
            result = {}
            cursor = connection.cursor()
            cursor.execute(catalog_def.sql_text)
            rows = cursor.fetch_all()
            if (len(rows) > 0):
                for row in rows:
                    result[row[0]] = row[1]
        return result

    @classmethod
    def find_list_by_catalog_id(cls, catalog_id: str, query=None) -> {}:
        result = []
        try:
            catalog_def = Catalog.objects.get(pk=catalog_id)
        except Catalog.DoesNotExist:
            return result
        if (catalog_def.content):
            result = ast.literal_eval(catalog_def.content)
            if (result and len(result) > 0):
                catalog = result
        elif (catalog_def.sql_text):
            # we have to execute a SQL to get it.
            cursor = connection.cursor()
            cursor.execute(catalog_def.sql_text)
            rows = cursor.fetch_all()
            if (len(rows) > 0):
                for row in rows:
                    catalog.append(row[0])
        return catalog

    class Meta:
        app_label = 'core'
        db_table = 'core_catalog'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
