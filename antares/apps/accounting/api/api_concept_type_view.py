""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""
import logging
import uuid

from django.db.models import Sum
from django.urls import reverse
from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView
from djmoney.money import Money

from antares.apps.client.models import Client
from antares.apps.core.constants import FieldDataType
from antares.apps.core.middleware.request import get_request
from antares.apps.core.models import ConceptType, concept_type
from antares.apps.core.models import SystemParameter
from antares.apps.core.manager import COPAD
from ..manager import AccountManager

from ..models import AccountBalance


logger = logging.getLogger(__name__)


class ApiConceptTypeView(BaseDatatableView):
    """ Retrieves a JSON formatted string to be used on the current account as the details by Concept Type. 
    
    :attribute model: The model in which is based the class (required by BaseDatatableView)
    :attribute columns: The columns to serve (required by BaseDatatableView)
    :attribute order_columns: The definition to allow ordering (required by BaseDatatableView)
    :attribute max_display_length: Max limit of records returned, this is used to protect our 
            site if someone tries to attack our site and make it return huge amount of data 
            (required by BaseDatatableView)
    :attribute default_currency: system-wide value  default currency
    :attribute default_locale: system-wide value default locale
    
    """
    model = AccountBalance
    columns = [
        'period',
        'principal_balance',
        'interest_balance',
        'penalties_balance',
        'total_balance',
    ]
    order_columns = [
        'period',
        'principal_balance',
        'interest_balance',
        'penalties_balance',
        'total_balance',
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
        if column == 'period':
            link_string = '<a onClick="display_accounting_panel(\'{client_id}\' , '+\
                   ' \'{full_name}\', null, null, \'{concept_type_id}\','+\
                '\'{concept_type_name}\', {period});\">{period}</a>'
            return link_string.format(
                client_id=self.client.id,
                full_name=self.client.full_name,
                concept_type_id=row.concept_type.id,
                concept_type_name=row.concept_type.concept_type_name,
                period=row.period)

        if column == 'principal_balance':
            if row.principal_balance__sum:
                return str(
                    Money(row.principal_balance__sum,
                          (row.default_currency or self.default_currency)))
            else:
                return str(
                    Money(0, (row.default_currency or self.default_currency)))
        if column == 'interest_balance':
            if row.interest_balance__sum:
                return str(
                    Money(row.interest_balance__sum,
                          (row.default_currency or self.default_currency)))
            else:
                return str(
                    Money(0, (row.default_currency or self.default_currency)))
        if column == 'penalties_balance':
            if row.penalties_balance__sum:
                return str(
                    Money(row.penalties_balance__sum,
                          (row.default_currency or self.default_currency)))
            else:
                return str(
                    Money(0, (row.default_currency or self.default_currency)))
        if column == 'total_balance':
            if row.total_balance__sum:
                return str(
                    Money(row.total_balance__sum,
                          (row.default_currency or self.default_currency)))
            else:
                return str(
                    Money(0, (row.default_currency or self.default_currency)))
        else:
            return super(ApiConceptTypeView, self).render_column(row, column)

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
        copad.client = self.client
        copad.concept_type = concept_type
        
        return AccountManager.find_balances_qs_by_COPAD(qs, copad)