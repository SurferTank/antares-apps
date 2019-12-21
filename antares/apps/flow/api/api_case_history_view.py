import logging

from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from antares.apps.core.enums import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter

from ..exceptions import FlowException
from ..models import FlowActivity

logger = logging.getLogger(__name__)


class ApiCaseHistoryView(BaseDatatableView):
    model = FlowActivity
    columns = [
        'id', 'activity_name', 'status', 'creation_date', 'start_date',
        'completion_date', 'performer'
    ]
    order_columns = ['id', '', 'status', 'creation_date', '', '', '']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def __init__(self):
        self.date_format_string = UserParameter.find_one(
            get_request().user, 'CORE_TEMPLATE_DATE_TIME_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d %H:%M')

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'id':
            if row.hrn_code:
                return row.hrn_code
            else:
                return str(row.id)

        elif column == 'activity_name':
            if row.activity_definition.display_name:
                return row.activity_definition.display_name
            elif row.activity_definition.activity_id:
                return row.activity_definition.activity_id
            else:
                return str(row.activity_definition.id)
        elif column == 'status':
            return row.status.label
        elif column == 'creation_date':
            return row.creation_date.strftime(self.date_format_string)
        elif column == 'start_date':
            if (row.start_date is not None):
                return row.start_date.strftime(self.date_format_string)
            else:
                return None
        elif column == 'completion_date':
            if (row.completion_date is not None):
                return row.completion_date.strftime(self.date_format_string)
            else:
                return None
        elif column == 'performer':
            if (row.performer.username is not None):
                try:
                    return row.performer.client.full_name
                except:
                    return row.performer.username

                return row.performer.username
            else:
                return ""
        else:
            return super(ApiCaseHistoryView, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        # simple example:
        activity_id = self.request.GET.get('activity_id', None)
        if activity_id:
            activity = FlowActivity.find_one(activity_id)
            if (activity is None):
                raise FlowException(
                    _(__name__ + ".exceptions.no_activity_was_found"))
            if (activity.performer != get_request().user):
                raise FlowException(
                    _(__name__ +
                      ".exceptions.this_activity_was_assigned_to_a_different_user"
                      ))
        else:
            raise FlowException(_(__name__ + ".no_activity_was_defined"))
        qs = qs.filter(flow_case=activity.flow_case)
        return qs
