import logging

from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from antares.apps.core.enums import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter
from antares.apps.document.enums import DocumentStatusType

from ..exceptions import FlowException
from ..models import FlowActivity
from ..models import FlowDocument

logger = logging.getLogger(__name__)


class ApiCaseDocumentView(BaseDatatableView):
    model = FlowDocument
    columns = [
        'relationship', 'document_id', 'form_definition', 'status',
        'creation_date', 'save_date', 'author', 'actions'
    ]
    order_columns = [
        'relationship', 'document.hrn_code', 'document.form_definition.id',
        'document.status', 'document.creation_date', 'document.save_date', '',
        ''
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def __init__(self):
        self.date_format_string = UserParameter.find_one(
            get_request().user, 'CORE_TEMPLATE_DATE_TIME_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d %H:%M')

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'document_id':
            if row.document.hrn_code:
                return row.document.hrn_code
            elif (row.document.id):
                return row.document.id
            else:
                return str(row.document.id)

        elif column == 'form_definition':
            if row.document.form_definition.id:
                return row.document.form_definition.id
            else:
                return None
        elif column == 'status':
            if row.document.status:
                return row.document.status.label
            else:
                return None

        elif column == 'relationship':
            if row.relationship:
                return row.relationship.label
            else:
                return None
        elif column == 'creation_date':
            if row.document.creation_date:
                return row.document.creation_date.strftime(
                    self.date_format_string)
            else:
                return None
        elif column == 'save_date':
            if row.document.save_date:
                return row.document.save_date.strftime(self.date_format_string)
            else:
                return None
        elif column == 'author':
            if row.document.author:
                try:
                    return row.document.author.client.full_name
                except:
                    return row.document.author.username
            else:
                return None
        elif column == 'actions':
            line = '<a href="#" onClick="viewWorkflowDocument(\''+ str(row.document.id) +\
                '\');"><i class="fa fa-eye" aria-hidden="true"></i></a>'
            line += '&nbsp;&nbsp;<a href="#" onClick="printWorkflowDocument(\''+ str(row.document.id) +\
                '\');"><i class="fa fa-print" aria-hidden="true"></i></a>'
            if DocumentStatusType.to_enum(
                    row.document.status) == DocumentStatusType.DRAFTED:
                line += '&nbsp;&nbsp;<a href="#" onClick="editWorkflowDocument(\''+ str(row.document.id) +\
                '\');"><i class="fa fa-pencil" aria-hidden="true"></i></a>'
            return line
        else:
            return super(ApiCaseDocumentView, self).render_column(row, column)

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
