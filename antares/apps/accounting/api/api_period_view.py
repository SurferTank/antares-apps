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
from antares.apps.core.models import ConceptType

from ..models import AccountBalance

logger = logging.getLogger(__name__)


class ApiPeriodView(BaseDatatableView):
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

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    def __init__(self):
        self.default_currency = SystemParameter.find_one(
            "CORE_DEFAULT_CURRENCY", FieldDataType.STRING, 'USD')
        self.default_locale = SystemParameter.find_one(
            "CORE_DEFAULT_LOCALE", FieldDataType.STRING, 'en_US')

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == 'period':
            #return '<a onClick="display_accounting_panel(\'' + str(self.client.id) + '\' , \'' + self.client.full_name + '\', null, null, \'' + \
            #        row.concept_type.id + '\', \'' + row.concept_type.concept_type_name + '\', ' + str(row.period) + ', \'' + str(row.account_type.id) +\
            #        '\', \'' + row.account_type.account_type_name + '\');\">' + \
            #        row.account_type.account_type_name + "</a>"
            link_string = '<a onClick="display_accounting_panel(\'{client_id}\' , '+\
                   ' \'{full_name}\', null, null, \'{concept_type_id}\','+\
                '\'{concept_type_name}\', {period}, \'{account_type_id}\', \'{account_type_name}\');\">{period}</a>'
            return link_string.format(
                client_id=self.client.id,
                full_name=self.client.full_name,
                concept_type_id=row.concept_type.id,
                concept_type_name=row.concept_type.concept_type_name,
                period=row.period,
                account_type_id=row.account_type.id,
                account_type_name=row.account_type.account_type_name)

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
            return super(ApiPeriodView, self).render_column(row, column)

    def filter_queryset(self, qs):
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
        qs = qs.filter(
            client=self.client,
            concept_type=self.concept_type,
            period=self.period)
        qs = qs.annotate(
            principal_balance__sum=Sum('principal_balance'),
            interest_balance__sum=Sum('interest_balance'),
            penalties_balance__sum=Sum('penalties_balance'),
            total_balance__sum=Sum('total_balance'))
        return qs
