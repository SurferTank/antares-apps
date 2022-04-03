from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


logger = logging.getLogger(__name__)


class Log(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))
    client = models.UUIDField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".client"),
        help_text=_(__name__ + ".client_help"))
    log_content = models.TextField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".log_content"),
        help_text=_(__name__ + ".primary_key_help"))
    document_header = models.UUIDField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".document_header"),
        help_text=_(__name__ + ".document_header_help"))
    flow_case = models.UUIDField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".flow_case"),
        help_text=_(__name__ + ".flow_case_help"))
    author = models.UUIDField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".author"),
        help_text=_(__name__ + ".author_help"))
    log_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_(__name__ + ".log_date"),
        help_text=_(__name__ + ".log_date_help"))
    log_key = models.CharField(
        max_length=400,
        verbose_name=_(__name__ + ".log_key"),
        help_text=_(__name__ + ".log_key_help"))
    system_module = models.CharField(
        max_length=400,
        verbose_name=_(__name__ + ".system_module"),
        help_text=_(__name__ + ".system_module_help"))
    post_date = models.DateTimeField(
        blank=True,
        null=True,
        editable=False,
        verbose_name=_(__name__ + ".post_date"),
        help_text=_(__name__ + ".post_date_help"))

    def save(self, *args, **kwargs):
        self.post_date = timezone.now()
        self.author = get_request().user.id
        super(Log, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    class Meta:
        app_label = 'core'
        db_table = 'core_log'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
