import logging
import uuid

from django.conf import settings
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class TerminalLog(models.Model):
    id = models.UUIDField(
        verbose_name=_(__name__ + '.id'),
        help_text=_(__name__ + '.id_help'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name=_(__name__ + '.author'),
        blank=True,
        null=True)
    post_date = models.DateTimeField(
        verbose_name=_(__name__ + '.post_date'),
        help_text=_(__name__ + '.post_date_help'))
    command = models.CharField(
        verbose_name=_(__name__ + '.command'),
        help_text=_(__name__ + '.command_help'),
        max_length=2000)
    result = models.TextField(
        verbose_name=_(__name__ + '.result'),
        help_text=_(__name__ + '.result_help'))

    def save(self, *args, **kwargs):
        self.post_date = timezone.now()
        self.author = get_request().user
        super(TerminalLog, self).save(*args, **kwargs)

    def __str__(self):
        return "Terminal record" + str(self.id)

    @staticmethod
    def log_terminal(actions, return_message):
        log = TerminalLog()
        log.command = actions
        log.result = return_message
        with transaction.atomic():
            log.save()

    class Meta:
        app_label = 'terminal'
        db_table = 'adm_terminal_log'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
