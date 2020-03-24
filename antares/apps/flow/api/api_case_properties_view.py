from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter
import logging

from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from ..constants import FlowBasicDataSubtype
from ..exceptions import FlowException
from ..models import FlowActivity, FlowProperty


logger = logging.getLogger(__name__)


class ApiCasePropertiesView(BaseDatatableView):
    model = FlowProperty
    columns = [
        'property_id',
        'value',
    ]
    order_columns = [
        'property_id',
        '',
    ]

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500

    def __init__(self):
        self.date_format_string = UserParameter.find_one(
            'CORE_TEMPLATE_DATE_TIME_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d %H:%M')

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'property_id':
            if row.property_definition.display_name:
                return row.property_definition.display_name
            elif (row.property_definition.property_id):
                return row.property_definition.property_id
            else:
                return str(row.id)

        elif column == 'value':
            if row.sub_data_type == FlowBasicDataSubtype.STRING:
                return row.string_value
            elif row.sub_data_type == FlowBasicDataSubtype.TEXT:
                return row.text_value
            elif row.sub_data_type == FlowBasicDataSubtype.DATE:
                if row.date_value:
                    return row.date_value.strftime(self.date_format_string)
                else:
                    return None
            elif row.sub_data_type == FlowBasicDataSubtype.INTEGER:
                if row.integer_value:
                    return str(row.integer_value)
                else:
                    return None
            elif row.sub_data_type == FlowBasicDataSubtype.FLOAT:
                if row.decimal_value:
                    return str(row.decimal_value)
                else:
                    return None
            elif row.sub_data_type == FlowBasicDataSubtype.BOOLEAN:
                if row.boolean_value == True:
                    return 'yes'
                elif row.boolean_value == False:
                    return 'no'
                else:
                    return ''
            else:
                raise FlowException(__name__ + 
                                    ".exceptions.not_implemented_yet")
        else:
            return super(ApiCasePropertiesView, self).render_column(
                row, column)

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
