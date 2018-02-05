from antares.apps.core.middleware.request import get_request
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from enumfields import EnumField
import logging
import uuid
from django.contrib.auth.models import AnonymousUser

from ..constants import ClientStatusType, ClientGenderType

logger = logging.getLogger(__name__)


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="client")
    code = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    registration_date = models.DateTimeField()
    birth_date = models.DateTimeField(blank=True, null=True)
    defunction_date = models.DateTimeField(blank=True, null=True)
    gender = EnumField(ClientGenderType, max_length=17, blank=True, null=True)
    status = EnumField(
        ClientStatusType, max_length=17, default=ClientStatusType.ACTIVE)
    client_type = models.ForeignKey(
        "ClientType", on_delete=models.PROTECT,
        db_column='client_type')  # Field name made lowercase.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="client_author_set",
        editable=False)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        from ..models import ClientBranch

        if self.creation_date is None:
            self.creation_date = timezone.now()
        if (not self.full_name and self.first_name and self.last_name):
            self.full_name = self.first_name
            if (self.middle_name):
                self.full_name += ' ' + self.middle_name
            self.full_name += ' ' + self.last_name
        if (self.registration_date is None):
            self.registration = timezone.now().date()
        self.update_date = timezone.now()
        if (get_request() is not None
                and isinstance(get_request().user, AnonymousUser) == False
                and self.author is None):
            self.author = get_request().user
        elif (get_request() is None
              or isinstance(get_request().user, AnonymousUser) == True):
            self.author = self.user
        super(Client, self).save(*args, **kwargs)

        # lets create the client branch 0 for the client, if it does not exist.
        branch = ClientBranch.find_one_by_client_and_branch_number(self, 0)
        if (branch is None):
            branch = ClientBranch()
            branch.branch_name = self.full_name
            branch.branch_number = 0
            branch.client = self
            branch.registration_date = self.registration_date
            branch.save()

    def __str__(self):
        if (self.code and self.full_name):
            return self.code + ' - ' + self.full_name
        elif (self.code and self.full_name is None):
            return self.code
        else:
            return str(self.id)

    @staticmethod
    def find_one(client_id):
        if isinstance(client_id, str):
            client_uuid = uuid.UUID(client_id)
        elif isinstance(client_id, uuid.UUID):
            client_uuid = client_id
        elif isinstance(client_id, Client):
            return client_id
        try:
            return Client.objects.get(id=client_uuid)
        except Client.DoesNotExist:
            return None

    @staticmethod
    def find_one_by_code(client_code):
        try:
            return Client.objects.get(code=client_code)
        except Client.DoesNotExist:
            return None

    def get_default_branch(self):
        try:
            return self.branch_set.select_related().filter(branch_number=0)
        except:
            return None

    class Meta:
        app_label = 'client'
        db_table = 'cli_client'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
