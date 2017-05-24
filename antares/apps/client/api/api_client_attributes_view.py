from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView
import logging
import uuid

from ..models import ClientAttribute, Client

logger = logging.getLogger(__name__)


class ApiClientAttributesView(BaseDatatableView):
    model = ClientAttribute
    columns = [
        'attribute_id',
        'value',
    ]
    order_columns = [
        'id',
        '',
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'attribute_id':
            if row.attribute_definition.display_name:
                return row.attribute_definition.display_name
            else:
                return str(row.id)

        elif column == 'value':
            data_type = FieldDataType.to_enum(row.data_type)

            if (data_type == FieldDataType.STRING):
                return row.string_value
            elif (data_type == FieldDataType.TEXT):
                return row.text_value
            elif (data_type == FieldDataType.DATE):
                return row.date_value.isoformat()
            elif (data_type == FieldDataType.INTEGER):
                return row.integer_value
            elif (data_type == FieldDataType.FLOAT):
                return row.float_value
            else:
                raise ValueError(__name__ + ".exceptions.not_implemented_yet")
        else:
            return super(ApiClientAttributesView, self).render_column(
                row, column)

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
