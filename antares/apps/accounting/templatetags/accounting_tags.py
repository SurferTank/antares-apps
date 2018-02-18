import logging
import babel.numbers
import decimal

from django import template
from django.utils.safestring import mark_safe
from antares.apps.core.models import SystemParameter
from antares.apps.core.constants import FieldDataType
from ..models import AccountBalance
from djmoney.money import Money

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
def total_accounting_balance(client):
    """ Returns the total balance for the given client 
    
    :param client: the client object
    :returns: the consolidated total balance of the client already formatted. 
    
    """
    default_currency = SystemParameter.find_one("DEFAULT_CURRENCY",
                                                FieldDataType.STRING, 'USD')
    default_locale = SystemParameter.find_one("CORE_DEFAULT_LOCALE",
                                              FieldDataType.STRING, 'en_US')
    result = AccountBalance.get_total_balance_by_client(client)
    if result is None:
        return str(Money(0, default_currency))
    else:
        return str(Money(result, default_currency))


@register.filter
def accounting_balance_status_image(client):
    """ Returns an image of the consolidated client's account status
    
    :param client: the client object
    :returns: the HTML string corresponding to the client's account status
    
    """
    result = AccountBalance.get_total_balance_by_client(client)
    if (result is None or result > 0):
        return mark_safe('<div style="text-align:center;"><font color="green" size="30">'+\
            '<i class="fa fa-check" aria-hidden="true"></i></font></div>')
    else:
        return mark_safe('<div style="text-align:center;"><font color="red" size="30">'+\
            '<i class="fa fa-times" aria-hidden="true"></i></font></div>')
