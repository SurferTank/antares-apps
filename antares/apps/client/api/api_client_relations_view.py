import logging
import uuid

from django.urls import reverse
from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter

from ..constants import ClientRelationType
from ..models import ClientUserRelation, Client


logger = logging.getLogger(__name__)


class ApiClientUserRelationsView(BaseDatatableView):
    model = ClientUserRelation
    columns = [
        'parent_user',
        'relation_type',
        'start_date',
        'end_date',
    ]
    order_columns = [
        'parent_user',
        'relation_type',
        'start_date',
        'end_date',
    ]
    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def __init__(self):
        self.date_format_string = UserParameter.find_one(
            'CORE_TEMPLATE_DATE_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d')

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'parent_user':
            return row.parent_user.username
        if column == 'relation_type':
            return ClientRelationType.to_enum(row.relation_type).get_label()
        if column == 'start_date':
            if (row.start_date is not None):
                return row.start_date.strftime(self.date_format_string)
            else:
                return None
        if column == 'end_date':
            if (row.end_date is not None):
                return row.end_date.strftime(self.date_format_string)
            else:
                return None
        else:
            return super(ApiClientUserRelationsView, self).render_column(
                row, column)

    def filter_queryset(self, qs):
        if (self.request.GET.get('client_id')):
            self.client = Client.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
        else:
            try:
                self.client = get_request().user.get_on_behalf_client()
            except:
                self.client = None
        qs = qs.filter(child_client=self.client)
        return qs
