import logging
from datetime import datetime, date

from django import template

from antares.apps.core.middleware.request import get_request

from ..constants import FieldDataType
from ..models import SystemParameter
from ..models import UserParameter

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter
def date_format(value):
    if (value is not None and
        (isinstance(value, datetime) or isinstance(value, date))):
        if get_request().user.is_anonymous() == False:
            date_format_string = UserParameter.find_one(
                get_request().user, 'CORE_TEMPLATE_DATE_FORMAT',
                FieldDataType.STRING, '%Y-%m-%d')
            if (date_format_string is not None):
                return value.strftime(date_format_string)
            else:
                return ""
        else:
            return value.strftime('%Y-%m-%d')
    else:
        return ""


@register.filter
def date_time_format(value):
    if (value is not None and
        (isinstance(value, datetime) or isinstance(value, date))):
        date_format_string = UserParameter.find_one(
            get_request().user, 'CORE_TEMPLATE_DATE_TIME_FORMAT',
            FieldDataType.STRING, "%Y-%m-%d %H:%M")
        if (date_format_string is not None):
            return value.strftime(date_format_string)
        else:
            return ""
    else:
        return ""
