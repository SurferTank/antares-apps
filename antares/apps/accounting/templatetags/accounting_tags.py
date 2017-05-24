import logging
import babel.numbers
import decimal

from django import template
from django.utils.safestring import mark_safe
from antares.apps.core.models import SystemParameter
from antares.apps.core.constants import FieldDataType
from ..models import AccountBalance

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
def total_accounting_balance(value):
    default_currency = SystemParameter.find_one("CORE_DEFAULT_CURRENCY",
                                                FieldDataType.STRING, 'USD')
    default_locale = SystemParameter.find_one("CORE_DEFAULT_LOCALE",
                                              FieldDataType.STRING, 'en_US')
    result = AccountBalance.get_total_balance_by_client(value)
    if result is None:
        return babel.numbers.format_currency(
            decimal.Decimal(0),
            currency=default_currency,
            locale=default_locale)
    else:
        return babel.numbers.format_currency(
            decimal.Decimal(result),
            currency=default_currency,
            locale=default_locale)


@register.filter
def accounting_balance_status_image(value):
    result = AccountBalance.get_total_balance_by_client(value)
    if (result is None or result > 0):
        return mark_safe('<div style="text-align:center;"><font color="green" size="30">'+\
            '<i class="fa fa-check" aria-hidden="true"></i></font></div>')
    else:
        return mark_safe('<div style="text-align:center;"><font color="red" size="30">'+\
            '<i class="fa fa-times" aria-hidden="true"></i></font></div>')
