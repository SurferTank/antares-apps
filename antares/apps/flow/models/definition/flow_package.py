import logging
import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings
from builtins import classmethod

logger = logging.getLogger(__name__)


class FlowPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)
    package_id = models.CharField(max_length=100)
    package_name = models.CharField(max_length=100)
    package_version = models.CharField(max_length=30)
    xpdl = models.TextField()

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(FlowPackage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @classmethod
    def find_one_by_package_id_and_package_version(cls, package_id,
                                                   package_version):
        try:
            return cls.objects.get(
                package_id=package_id, package_version=package_version)
        except FlowPackage.DoesNotExist:
            return None

    @classmethod
    def find_all(cls):
        return cls.objects.all()

    @classmethod
    def find_one_by_id(cls, flow_id):
        try:
            return cls.objects.get(id=flow_id)
        except cls.DoesNotExist:
            return None

    class Meta:
        app_label = 'flow'
        db_table = 'flow_package'
        unique_together = (("package_id", "package_version"), )
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
