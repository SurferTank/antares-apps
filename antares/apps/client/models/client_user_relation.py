import logging
import uuid

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from antares.apps.core.middleware.request import get_request
from django.conf import settings

from ..exceptions import ClientException
from antares.apps.client.enums import ClientRelationType

logger = logging.getLogger(__name__)


class ClientUserRelation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="client_user_relation_set",
        db_column='parent_user',
        null=True)
    child_client = models.ForeignKey(
        "Client",
        on_delete=models.PROTECT,
        related_name='child_client_relation_set',
        db_column='child_client')
    relation_type   = models.CharField(
        max_length=20,
        choices=ClientRelationType.choices
    )
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)
    creation_date = models.DateTimeField(blank=True, null=True, editable=False)
    update_date = models.DateTimeField(blank=True, null=True, editable=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="client_user_relation_author_set",
        blank=True,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        if self.creation_date is None:
            self.creation_date = timezone.now()
        self.update_date = timezone.now()
        self.author = get_request().user
        super(ClientUserRelation, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def get_child_client_list(clients_only=True, only_executive=True):
        """
        Gets the clients the user has relations with. Bear in mind that setting client_lists to false will not return
            the user's client.
        """
        client_list = []
        if (clients_only):
            if (get_request().user.client is not None):
                client_list.append(get_request().user.client)
            else:
                raise ClientException(
                    _(__name__ + '.exceptions.user_has_no_client_assigned'))

            for client_relation in ClientUserRelation.objects.filter(
                    Q(parent_user=get_request().user) &
                (Q(start_date__lte=timezone.now()) &
                 (Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True)))
            ):
                if ((only_executive == True and
                     ClientRelationType.to_enum(client_relation.relation_type)
                     != ClientRelationType.GENERIC_WORKER)
                        or only_executive == False):
                    client_list.append(client_relation.child_client)
        else:
            for client_relation in ClientUserRelation.objects.filter(
                    Q(parent_user=get_request().user) & Q(
                        start_date__lte=timezone.now()) &
                (Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True))):
                if ((only_executive == True and
                     ClientRelationType.to_enum(client_relation.relation_type)
                     != ClientRelationType.GENERIC_WORKER)
                        or only_executive == False):
                    client_list.append(client_relation)
        return client_list

    class Meta:
        app_label = 'client'
        db_table = 'cli_user_client_relation'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
