import logging

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request


logger = logging.getLogger(__name__)


class AccountType(models.Model):
    id = models.SlugField(primary_key=True, max_length=255)
    active = models.BooleanField(default=True)
    auxiliary_account = models.BooleanField(default=False)
    description = RichTextField(blank=True, null=True)
    exigible = models.BooleanField(default=False)
    include_interest = models.BooleanField(default=False)
    include_penalties = models.BooleanField(default=False)
    account_type_name = models.CharField(max_length=100)
    hrn_script = models.TextField(blank=True, null=True)
    is_document_based = models.BooleanField(default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        editable=False)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(AccountType, self).save(*args, **kwargs)

    def __str__(self):
        return self.id

    @classmethod
    def find_one(cls, account_type_id):
        try:
            return cls.objects.get(id=account_type_id)
        except cls.DoesNotExist:
            return None

    class Meta:
        app_label = 'accounting'
        db_table = 'acc_account_type'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
