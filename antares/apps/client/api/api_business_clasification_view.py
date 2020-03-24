from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter
import logging
import uuid

from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from ..constants import ItemStatusType, AddressType
from ..models import ClientBusinessClassification, ClientBranch


logger = logging.getLogger(__name__)


class ApiBranchListBusinessClassificationView(BaseDatatableView):
    model = ClientBusinessClassification
    columns = [
        'business_classification',
        'start_date',
        'end_date',
    ]
    order_columns = [
        'business_classification',
        'start_date',
        'end_date',
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def __init__(self):
        self.date_format_string = UserParameter.find_one(
            get_request().user, 'CORE_TEMPLATE_DATE_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d')

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'business_classification':
            if row.business_classification.business_classification_name is not None:
                return row.business_classification.business_classification_name
            elif row.business_classification.business_classification_code is not None:
                return row.business_classification.business_classification_code
            else:
                return None

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
            return super(ApiBranchListBusinessClassificationView,
                         self).render_column(row, column)

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
