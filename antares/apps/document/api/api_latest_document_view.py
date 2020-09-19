""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""

from antares.apps.client.models import Client
from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import SystemParameter
from antares.apps.core.models import UserParameter
from antares.apps.user.exceptions.user_exception import UserException
import decimal
import logging
import uuid

import babel.numbers
from django.db.models import Q
from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from ..models import DocumentHeader


logger = logging.getLogger(__name__)


class ApiLatestDocumentView(BaseDatatableView):
    """ Retrieves a JSON formatted string to be used on the document latest document control
    
   
    
    """
    model = DocumentHeader
    columns = [
        'id',
        'form_definition',
       'author',
       'status',
       'save_date',
       'actions'
    ]
    order_columns = [
        'id',
        'form_definition',
        'author',
       'status',
       'save_date',
       
    ]

    max_display_length = 5
  
    def __init__(self):
        """ Initial value settings 
        """
        self.default_currency = SystemParameter.find_one(
            "DEFAULT_CURRENCY", FieldDataType.STRING, 'USD')
        self.default_locale = SystemParameter.find_one(
            "DEFAULT_LOCALE", FieldDataType.STRING, 'en_US')
        self.date_format_string = UserParameter.find_one('CORE_TEMPLATE_DATE_FORMAT',
            FieldDataType.STRING, '%Y-%m-%d')

    def render_column(self, row, column):
        """ Overriden method to render a column (a hook on BaseDatatableView)
        """
        if column == 'id':
            if row.hrn_code:
                return row.hrn_code
            else:
                return str(row.id)
        if column == 'save_date':
            if row.save_date is not None:
                return row.save_date.strftime(self.date_format_string)
            elif row.draft_date is not None:
                return row.draft_date.strftime(self.date_format_string)
            else:
                return ""
        else:
            return super(ApiLatestDocumentView, self).render_column(row, column)

    def filter_queryset(self, qs):
        """ Overriden method to modify the query to retrieve the correct data (a hook on BaseDatatableView)
        """
        if (self.request.GET.get('client_id')):
            self.client = Client.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
            if (self.client is None):
                raise ValueError(
                    _(__name__ + '.exceptions.client_does_not_exist'))
        else:
            try:
                self.client = get_request().user.get_on_behalf_client()
            except UserException:
                return qs
        if(self.client is None):
            qs = qs.filter(Q(status="INVALID"))
        else:
            qs = qs.filter(Q(client=self.client) | Q(author=get_request().user)).order_by("-save_date")
        return qs
