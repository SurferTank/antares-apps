from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter
import logging

from django.utils.translation import gettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from ..exceptions import FlowException
from ..models import FlowNote, FlowActivity


logger = logging.getLogger(__name__)


class ApiCaseNoteListView(BaseDatatableView):
    model = FlowNote
    columns = ['post_date', 'author', 'title', 'actions']
    order_columns = ['post_date', 'author.client.full_name', 'title', '']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def __init__(self):
        self.date_format_string = UserParameter.find_one('CORE_TEMPLATE_DATE_TIME_FORMAT',
                                                         FieldDataType.STRING, '%Y-%m-%d %H:%M')

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'post_date':
            if row.post_date:
                return row.post_date.strftime(self.date_format_string)
        elif column == 'author':
            if row.author:
                try:
                    return row.author.client.full_name
                except:
                    return row.author.username
            else:
                return None
        elif column == 'title':
            if (row.title and len(row.title) < 30):
                return row.title
            else:
                return row.title[:30] + "[...]"
        elif column == 'actions':
            line = '<a href="#" onClick="editNote(\'' + str(row.id) + \
                '\', \'' + row.title + '\', \'' + row.content + \
                '\', \'' + str(row.flow_case.id) + \
                '\');"><i class="fa fa-pencil-alt" aria-hidden="true"></i></a>'
            return line
        else:
            return super(ApiCaseNoteListView, self).render_column(row, column)

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
