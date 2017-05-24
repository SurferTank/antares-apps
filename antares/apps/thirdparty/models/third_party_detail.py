import logging
import uuid

from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings
from ..constants import ThirdPartyDetailStatusType
from enumfields import EnumField

logger = logging.getLogger(__name__)


class ThirdPartyDetail(models.Model):
    id = models.UUIDField(
        verbose_name=_(__name__ + '.id'),
        help_text=_(__name__ + '.id_help'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    third_party_record = models.ForeignKey(
        'ThirdPartyRecord',
        on_delete=models.PROTECT,
        db_column='third_party_record',
        related_name='detail_set')
    reported_branch = models.ForeignKey(
        'client.ClientBranch',
        on_delete=models.PROTECT,
        db_column='reported_branch')
    document = models.ForeignKey(
        'document.DocumentHeader',
        on_delete=models.PROTECT,
        db_column='document')
    status = EnumField(
        ThirdPartyDetailStatusType,
        max_length=30,
        default=ThirdPartyDetailStatusType.OPEN)
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        db_column='author',
        related_name='third_party_detail_author_set')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ThirdPartyDetail, self).save(*args, **kwargs)

    class Meta:
        app_label = 'third_party'
        db_table = 'third_party_detail'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
