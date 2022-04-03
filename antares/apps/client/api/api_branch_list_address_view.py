from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.utils.translation import gettext as _
from ajax_datatable.views import AjaxDatatableView as BaseDatatableView

from ..constants import ItemStatusType, AddressType
from ..models import AddressItem, ClientBranch


logger = logging.getLogger(__name__)


class ApiBranchListAddressView(BaseDatatableView):
    model = AddressItem
    columns = [
        'address_type',
        'country',
        'line_1',
        'line_2',
        'postal_code',
        'is_active',
        'status',
    ]
    order_columns = [
        'address_type',
        'country',
        'line_1',
        'line_2',
        'postal_code',
        'is_active',
        'status',
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'address_type':
            address_type = AddressType.to_enum(row.address_type)
            if address_type is not None:
                return address_type.label
            else:
                return None

        elif column == 'country':
            if (row.country_code):
                return row.country_code
            else:
                return None

        elif column == 'line_1':
            if (row.line_1):
                return row.line_1
            else:
                return None
        elif column == 'line_2':
            if (row.line_2):
                return row.line_2
            else:
                return None
        elif column == 'postal_code':
            if (row.postal_code):
                return row.postal_code
            else:
                return None
        elif column == 'is_principal':
            if (row.is_principal == True):
                return _('True')
            else:
                return _('False')
        elif column == 'status':
            status = ItemStatusType.to_enum(row.status)
            if (status is not None):
                return status.label
            else:
                return None
        else:
            return super(ApiBranchListAddressView, self).render_column(
                row, column)

    def filter_queryset(self, qs):
        if (self.request.GET.get('branch_id')):
            self.branch = ClientBranch.find_one(
                uuid.UUID(self.request.GET.get('branch_id')))
            if (self.branch is None):
                raise ValueError(
                    _(__name__ + '.exceptions.branch_does_not_exist'))
        else:
            try:
                self.branch = get_request().user.get_on_behalf_client(
                ).get_default_branch()
            except:
                self.branch = None

        qs = qs.filter(client_branch=self.branch)
        return qs
