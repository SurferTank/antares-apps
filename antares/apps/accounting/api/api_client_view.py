""" 
Copyright 2013-2017 SurferTank Inc. 

Original version by Leonardo Belen<leobelen@gmail.com>
"""
import logging
import uuid
import babel.numbers
import decimal

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.utils.translation import ugettext as _
from django_datatables_view.base_datatable_view import BaseDatatableView
from antares.apps.core.models import SystemParameter
from antares.apps.core.constants import FieldDataType

from antares.apps.client.models import Client
from antares.apps.core.middleware.request import get_request

from ..models import AccountBalance
from antares.apps.user.exceptions.user_exception import UserException

logger = logging.getLogger(__name__)


class ApiClientView(BaseDatatableView):
    """ Retrieves a JSON formatted string to be used on the current account as the front page. 
    
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
        'concept_type',
        'principal_balance',
        'interest_balance',
        'penalties_balance',
        'total_balance',
    ]
    order_columns = [
        'concept_type',
        'principal_balance',
        'interest_balance',
        'penalties_balance',
        'total_balance',
    ]
    client = None
    
    max_display_length = 50
    
    default_currency = None
    
    default_locale  = None

    def __init__(self):
        """ Initial value settings 
        """
        self.default_currency = SystemParameter.find_one(
            "CORE_DEFAULT_CURRENCY", FieldDataType.STRING, 'USD')
        self.default_locale = SystemParameter.find_one(
            "CORE_DEFAULT_LOCALE", FieldDataType.STRING, 'en_US')

    def render_column(self, row, column):
        """ Overriden method to render a column (a hook on BaseDatatableView)
        """
        # We want to render user as a custom column
        if column == 'concept_type':
            if row.concept_type.concept_type_name:
                link_string = '<a onClick="display_accounting_panel(\'{client_id}\' , '+\
                    ' \'{full_name}\', null, null, \'{concept_type_id}\','+\
                    '\'{concept_type_name}\');\">{concept_type_name}</a>'
                return link_string.format(
                    client_id=self.client.id,
                    full_name=self.client.full_name,
                    concept_type_id=row.concept_type.id,
                    concept_type_name=row.concept_type.concept_type_name)

        if column == 'principal_balance':
            if row.principal_balance__sum:
                return babel.numbers.format_currency(
                    decimal.Decimal(row.principal_balance__sum),
                    currency=self.default_currency,
                    locale=self.default_locale)
            else:
                return babel.numbers.format_currency(
                    decimal.Decimal(0),
                    currency=self.default_currency,
                    locale=self.default_locale)
        if column == 'interest_balance':
            if row.interest_balance__sum:
                return babel.numbers.format_currency(
                    decimal.Decimal(row.interest_balance__sum),
                    currency=self.default_currency,
                    locale=self.default_locale)
            else:
                return babel.numbers.format_currency(
                    decimal.Decimal(0),
                    currency=self.default_currency,
                    locale=self.default_locale)
        if column == 'penalties_balance':
            if row.penalties_balance__sum:
                return babel.numbers.format_currency(
                    decimal.Decimal(row.penalties_balance__sum),
                    currency=self.default_currency,
                    locale=self.default_locale)
            else:
                return babel.numbers.format_currency(
                    decimal.Decimal(0),
                    currency=self.default_currency,
                    locale=self.default_locale)
        if column == 'total_balance':
            if row.total_balance__sum:
                return babel.numbers.format_currency(
                    decimal.Decimal(row.total_balance__sum),
                    currency=self.default_currency,
                    locale=self.default_locale)
            else:
                return babel.numbers.format_currency(
                    decimal.Decimal(0),
                    currency=self.default_currency,
                    locale=self.default_locale)
        else:
            return super(ApiClientView, self).render_column(row, column)

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

        qs = qs.filter(client=self.client)
        qs = qs.annotate(
            principal_balance__sum=Sum('principal_balance'),
            interest_balance__sum=Sum('interest_balance'),
            penalties_balance__sum=Sum('penalties_balance'),
            total_balance__sum=Sum('total_balance'))
        return qs
