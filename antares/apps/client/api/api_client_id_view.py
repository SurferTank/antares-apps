from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from ..constants import ItemStatusType
from ..models import IdentificationItem, Client


logger = logging.getLogger(__name__)


class ApiClientIdView(BaseDatatableView):
    model = IdentificationItem
    columns = [
        'type',
        'code',
        'status',
    ]
    order_columns = [
        'type',
        'code',
        'status',
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'type':
            if row.type.id is not None:
                return row.type.id
            else:
                return None

        elif column == 'code':
            if (row.code):
                return row.code
            else:
                return None
        elif column == 'status':
            status = ItemStatusType.to_enum(row.status)
            if (status is not None):
                return status.label
            else:
                return None
        else:
            return super(ApiClientIdView, self).render_column(row, column)

    def filter_queryset(self, qs):
        if (self.request.GET.get('client_id')):
            self.client = Client.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
            if (self.client is None):
                raise ValueError(
                    _(__name__ + '.exceptions.client_does_not_exist'))
        else:
            try:
                self.client = get_request().user.get_on_behalf_client()
            except:
                self.client = None
        qs = qs.filter(client=self.client)
        return qs
