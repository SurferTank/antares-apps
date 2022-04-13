'''
Created on 21/8/2016

@author: leobelen
'''
from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import UserParameter
from antares.apps.flow.exceptions.flow_exception import FlowException
import logging

from django.urls import reverse
from django.utils.translation import gettext as _
from ajax_datatable.views import AjaxDatatableView

from ..constants import FlowActivityStatusType
from ..models import FlowActivity


logger = logging.getLogger(__name__)


class ApiInboxCreatedCasesView(AjaxDatatableView):
    model = FlowActivity
    title = 'Activities'
    #initial_order = [['creation_date', 'desc'], ]
    #search_values_separator = '+'

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'case_name', 'visible': True, },
        {'name': 'priority',  'visible': True, },
        {'name': 'source_id', 'visible': True, },
        {'name': 'creation_date', 'visible': True, },
        {'name': 'actions', 'visible': True, }
    ]
    # columns = [
    #    'id', 'case_id', 'case_name', 'priority', 'source_id', 'creation_date',
    #    'actions'
    # ]
    #order_columns = ['id', '', '', '', '', '', '']

    # def __init__(self):
    #    self.date_format_string = UserParameter.find_one(
    #        'CORE_TEMPLATE_DATE_TIME_FORMAT',
    #        FieldDataType.STRING, '%Y-%m-%d %H:%M')
