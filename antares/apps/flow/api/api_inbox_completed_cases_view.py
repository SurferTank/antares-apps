'''
Created on 21/8/2016

@author: leobelen
'''
import logging

from django.urls import reverse
from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter
from antares.apps.flow.exceptions.flow_exception import FlowException

from ..constants import FlowActivityStatusType
from ..models import FlowActivity


logger = logging.getLogger(__name__)


class ApiInboxCompletedCasesView(BaseDatatableView):
    model = FlowActivity
    columns = [
        'id', 'case_id', 'case_name', 'priority', 'source_id', 'creation_date',
        'start_date', 'completion_date', 'actions'
    ]
    order_columns = ['id', '', '', '', '', '', '', '', '']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def __init__(self):
        self.date_format_string = UserParameter.find_one(
            get_request().user, 'CORE_TEMPLATE_DATE_TIME_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d %H:%M')

    def render_column(self, row, column):
        if column == 'id':
            if row.hrn_code:
                return row.hrn_code
            else:
                return str(row.id)
        elif column == 'case_id':
            if row.flow_case.hrn_code:
                return row.flow_case.hrn_code
            else:
                return str(row.flow_case.id)
        elif (column == 'case_name'):
            if row.flow_case.case_name:
                return row.flow_case.case_name
            else:
                return None
        elif (column == 'priority'):
            if (row.flow_case.priority):
                return row.flow_case.priority
            else:
                return None
        elif (column == 'source_id'):
            if (row.flow_case.source is not None):
                if (row.flow_case.source.document.hrn_code is not None):
                    return row.flow_case.source.document.hrn_code
                else:
                    return str(row.flow_case.source.document.id)
            else:
                return ""
        elif (column == 'creation_date'):
            return row.creation_date.strftime(self.date_format_string)

        elif (column == 'start_date'):
            if row.start_date is not None:
                return row.start_date.strftime(self.date_format_string)
            else:
                return None

        elif (column == 'completion_date'):
            if row.completion_date is not None:
                return row.completion_date.strftime(self.date_format_string)
            else:
                return None

        elif (column == 'actions'):
            return '<a href="' + reverse("antares.apps.flow:dashboard_view", args=[str(row.id)]) + '">' + \
                '<i class="fa fa-sign-in" aria-hidden="true"></i></a>'
        else:
            return super(ApiInboxCompletedCasesView, self).render_column(
                row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        # simple example:
        qs = FlowActivity.find_by_perfomer_and_status(
            get_request().user, FlowActivityStatusType.COMPLETED)
        return qs
