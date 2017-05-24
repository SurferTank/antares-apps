'''
Created on Jul 22, 2016

@author: leobelen
'''
from datetime import datetime
import logging

from django.utils.translation import ugettext as _

from ..constants import FieldDataType, TimeUnitType
from ..models import SystemParameter, Holiday

logger = logging.getLogger(__name__)


class PeriodManager(object):
    """
    Processes periods in an unified way, setting rules for all modules to follow.
    The idea here is to follow these conventions by Time unit
    Year:
        4 digits - Valid number greater than 1970 (epoch time) - year.
        Total: 4 digits

    Month:
        4 digits - Valid number greater than 1970 (epoch time) - year.
        2 digits zero padded - valid digit between 1 and 12 - Month
        Total: 6 digits
    Day:
        4 digits - Valid number greater than 1970 (epoch time) - year.
        2 digits zero padded - valid digit between 1 and 12 - Month
        2 digits zero padded - valid digit between 1 and 31 - Day
        Total: 8 digits - Has to make a valid date.
    """

    def __init__(self, params):
        '''
        Constructor
        '''
        pass

    @classmethod
    def validate_period_and_time_unit(cls, period, time_unit=None):
        """ validates a period to make sure it is pertaining to a valid date """
        if time_unit is None:
            time_unit = cls.get_time_unit_from_period(period)
        if (time_unit == TimeUnitType.YEAR):
            if (len(str(period)) != 4):
                raise ValueError(_(__name__ + '.incorrect_period_format'))
            if (int(float(period)) < 1970):
                raise ValueError(_(__name__ + '.years_cannot_be_before_1970'))
        elif (time_unit == TimeUnitType.MONTH):
            if (len(str(period)) != 6):
                raise ValueError(_(__name__ + '.incorrect_period_format'))
            year = int(float(str(period)[:4]))
            month = int(float(str(period)[4:]))
            if (year < 1970):
                raise ValueError(_(__name__ + '.years_cannot_be_before_1970'))
            if (month < 1 or month > 12):
                raise ValueError(_(__name__ + '.month_is_out_of_range'))
        elif (time_unit == TimeUnitType.DAY):
            if (len(str(period)) != 8):
                raise ValueError(
                    _(__name__ + '.period.incorrect_period_format'))
            year = int(float(str(period)[:4]))
            month = int(float(str(period)[2:-4]))
            day = int(float(str(period)[6:]))
            if (year < 1970):
                raise ValueError(_(__name__ + '.years_cannot_be_before_1970'))
            if (month < 1 or month > 12):
                raise ValueError(_(__name__ + '.month_is_out_of_range'))
            if (day < 1 or day > 31):
                raise ValueError(_(__name__ + '.month_is_out_of_range'))
            try:
                datetime(year, month, day)
            except:
                raise ValueError(
                    _(__name__ + '.period_does_not_conform_a_valid_date'))
        else:
            raise NotImplementedError

    @classmethod
    def calculate_date_from_period(cls,
                                   base_date,
                                   period,
                                   time_unit=None,
                                   consider_saturdays=True,
                                   consider_sundays=True,
                                   consider_holidays=True):
        if time_unit is None:
            time_unit = cls.get_time_unit_from_period(period)

        cls.validate_period_and_time_unit(period, time_unit)

        if (time_unit == TimeUnitType.YEAR):
            start_at_midnight = SystemParameter.find_one(
                "YEAR_PERIOD_STARTS_AT_MIDNIGHT", FieldDataType.BOOLEAN, True)
            year = int(float(str(period)[:4]))
            if (start_at_midnight == True):
                base_date = datetime(year, base_date.month, base_date.day, 0,
                                     0, 0, 0, base_date.tzinfo)
            else:
                base_date = datetime(year, base_date.month, base_date.day,
                                     base_date.hour, base_date.minute,
                                     base_date.second, base_date.microsecond,
                                     base_date.tzinfo)
            return Holiday.next_day(base_date, consider_saturdays,
                                    consider_sundays, consider_holidays)
        if (time_unit == TimeUnitType.MONTH):
            start_at_midnight = SystemParameter.find_one(
                "MONTH_PERIOD_STARTS_AT_MIDNIGHT", FieldDataType.BOOLEAN, True)
            year = int(float(str(period)[:4]))
            month = int(float(str(period)[4:]))
            if (start_at_midnight == True):
                base_date = datetime(year, month, base_date.day, 0, 0, 0, 0,
                                     base_date.tzinfo)
            else:
                base_date = datetime(year, month, base_date.day,
                                     base_date.hour, base_date.minute,
                                     base_date.second, base_date.microsecond,
                                     base_date.tzinfo)
            return Holiday.next_day(base_date, consider_saturdays,
                                    consider_sundays, consider_holidays)
        if (time_unit == TimeUnitType.DAY):
            start_at_midnight = SystemParameter.find_one(
                "DAY_PERIOD_STARTS_AT_MIDNIGHT", FieldDataType.BOOLEAN, True)
            year = int(float(str(period)[:4]))
            month = int(float(str(period)[2:-4]))
            day = int(float(str(period)[6:]))
            if (start_at_midnight == True):
                base_date = datetime(year, month, day, 0, 0, 0, 0,
                                     base_date.tzinfo)
            else:
                base_date = datetime(year, month, day, base_date.hour,
                                     base_date.minute, base_date.second,
                                     base_date.microsecond, base_date.tzinfo)
            return Holiday.next_day(base_date, consider_saturdays,
                                    consider_sundays, consider_holidays)

    @classmethod
    def get_time_unit_from_period(cls, period):
        """gets the time unit used to construct the period, based on its length """
        if len(str(period)) == 4:
            return TimeUnitType.YEAR
        elif len(str(period)) == 6:
            return TimeUnitType.MONTH
        elif len(str(period)) == 8:
            return TimeUnitType.DAY

        raise ValueError

    @classmethod
    def get_one_by_concept_type_id_and_period(cls, period, concept_type):
        from antares.apps.document.models.form_definition import FormDefinition
        return FormDefinition.get_one_by_concept_type_id_and_period(
            period, concept_type)
