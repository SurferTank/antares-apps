from antares.apps.core.middleware.request import get_request
import logging
import uuid

from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from ..constants import ItemStatusType, TelephoneItemType
from ..models import TelephoneItem, ClientBranch


logger = logging.getLogger(__name__)


class ApiBranchListTelephoneView(BaseDatatableView):
    model = TelephoneItem
    columns = [
        'telephone_type',
        'telephone',
        'is_principal',
        'status',
    ]
    order_columns = [
        'telephone_type',
        'telephone',
        'is_principal',
        'status',
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'telephone_type':
            telephone_type = TelephoneItemType.to_enum(row.telephone_type)
            if telephone_type is not None:
                return telephone_type.get_label()
            else:
                return None
        elif column == 'telephone':
            if (row.telephone):
                return row.telephone
            else:
                return None
        elif column == 'is_principal':
            if (row.is_principal == True):
                return _("True")
            else:
                return _("False")
        elif column == 'status':
            status = ItemStatusType.to_enum(row.status)
            if (status is not None):
                return status.get_label()
            else:
                return None
        else:
            return super(ApiBranchListTelephoneView, self).render_column(
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
