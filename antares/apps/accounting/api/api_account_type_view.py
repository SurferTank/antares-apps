""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""

import decimal
import logging
import uuid

import babel.numbers
from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView

from antares.apps.client.models import Client
from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import ConceptType
from antares.apps.core.models import SystemParameter

from ..models import AccountTransaction, AccountType
from antares.apps.core.manager import COPAD
from ..manager import AccountManager

logger = logging.getLogger(__name__)


class ApiAccountTypeView(BaseDatatableView):
    """ Retrieves a JSON formatted string to be used on the current account as the details by Account Type. 
    
    :attribute model: The model in which is based the class (required by BaseDatatableView)
    :attribute columns: The columns to serve (required by BaseDatatableView)
    :attribute order_columns: The definition to allow ordering (required by BaseDatatableView)
    :attribute max_display_length: Max limit of records returned, this is used to protect our 
            site if someone tries to attack our site and make it return huge amount of data 
            (required by BaseDatatableView)
    :attribute default_currency: system-wide value  default currency
    :attribute default_locale: system-wide value default locale
    
    """
    model = AccountTransaction
    columns = [
        'id',
        'document_id',
        'transaction_type',
        'effect',
        'principal_amount',
        'interest_amount',
        'penalties_amount',
        'total_amount',
    ]
    order_columns = [
        'id',
        '',
        '',
        '',
        'principal_amount',
        'interest_amount',
        'penalties_amount',
        'total_amount',
    ]

    max_display_length = 50

    default_currency = None

    default_locale = None

    def __init__(self):
        """ Initial value settings 
        """
        self.default_currency = SystemParameter.find_one(
            "DEFAULT_CURRENCY", FieldDataType.STRING, 'USD')
        self.default_locale = SystemParameter.find_one(
            "DEFAULT_LOCALE", FieldDataType.STRING, 'en_US')

    def render_column(self, row, column):
        """ Overriden method to render a column (a hook on BaseDatatableView)
        """
        if column == 'id':
            if row.hrn_code:
                return row.hrn_code
            else:
                return str(row.id)
        if column == 'document_id':
            row_string = '{document_name}&nbsp;<a href="#" onClick="view_accounting_document(\''+\
                '{document_id}\');"><i class="fa fa-eye" aria-hidden="true"></i></a>'
            if (row.account_document.document is not None):
                if row.account_document.document.hrn_code:
                    return row_string.format(
                        document_id=row.account_document.document.id,
                        document_name=row.account_document.document.hrn_code)
                else:
                    return row_string.format(
                        document_id=row.account_document.document.id,
                        document_name=row.account_document.document.id)
            else:
                return None
        if column == 'transaction_type':
            if row.transaction_type.transaction_type_name:
                return row.transaction_type.transaction_type_name
            else:
                return str(row.transaction_type.id)
        if column == 'effect':
            return row.transaction_type.effect.label
        if column == 'principal_amount':
            return str(row.principal_amount)
        if column == 'interest_amount':
            return str(row.interest_amount)
        if column == 'penalties_amount':
            return str(row.penalties_amount)
        if column == 'total_amount':
            return str(row.total_amount)
        else:
            return super(ApiAccountTypeView, self).render_column(row, column)

    def filter_queryset(self, qs):
        """ Overriden method to modify the query to retrieve the correct data (a hook on BaseDatatableView)
        """
        copad = COPAD()
        if (self.request.GET.get('client_id')):
            self.client = Client.find_one(
                uuid.UUID(self.request.GET.get('client_id')))
            if (self.client is None):
                raise ValueError(
                    _(__name__ + '.exceptions.client_does_not_exist'))
        else:
            self.client = get_request().user.get_on_behalf_client()
        if (self.request.GET.get('concept_type_id')):
            self.concept_type = ConceptType.find_one(
                self.request.GET.get('concept_type_id'))
            if (self.concept_type is None):
                raise ValueError(
                    _(__name__ + '.exceptions.concept_type_does_not_exist'))
        else:
            raise ValueError(
                _(__name__ + '.exceptions.concept_type_is_undefined'))
        if (self.request.GET.get('period')):
            self.period = self.request.GET.get('period')
        else:
            raise ValueError(_(__name__ + '.exceptions.period_is_undefined'))
        if (self.request.GET.get('account_type_id')):
            self.account_type = AccountType.find_one(
                self.request.GET.get('account_type_id'))
            if (self.account_type is None):
                raise ValueError(
                    _(__name__ + '.exceptions.account_type_does_not_exist'))
        else:
            raise ValueError(
                _(__name__ + '.exceptions.account_type_is_undefined'))
        copad.client = self.client 
        copad.concept_type = self.concept_type 
        copad.period = self.period
        copad.account_type = self.account_type
        
        qs =  AccountManager.find_balances_qs_by_COPAD(qs, copad)
        return qs
