import logging

from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

from ..enums import TransactionEffectType

logger = logging.getLogger(__name__)


class TransactionType(models.Model):
    id = models.SlugField(primary_key=True, max_length=40)
    inverse_transaction_type = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        db_column='inverse_transaction_type',
        blank=True,
        null=True)
    active = models.BooleanField(default=True)
    calculate_charges = models.BooleanField(default=True)
    description = RichTextField(blank=True, null=True)
    effect = models.CharField(choices=TransactionEffectType, max_length=6)
    transaction_type_name = models.CharField(max_length=100)
    post_zeros = models.BooleanField(default=True)
    hrn_script = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)
    creation_date = models.DateTimeField(null=True, editable=False)
    update_date = models.DateTimeField(null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(TransactionType, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_transaction_type'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
