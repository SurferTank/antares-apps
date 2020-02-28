'''
Created on Jul 22, 2016

@author: leobelen
'''
from datetime import datetime
import logging
import calendar
from django.utils import timezone

from django.utils.translation import ugettext as _

from ..constants import FieldDataType, TimeUnitType
from ..models.holiday import Holiday
from ..models.system_parameter import SystemParameter
from antares.apps.client.constants import ClientStatusType
from dateutil.relativedelta import relativedelta

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
        """ 
        Validates a period to make sure it is pertaining to a valid date 
        """
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
                base_date = timezone.datetime(year, base_date.month, base_date.day, 0,
                                     0, 0, 0, base_date.tzinfo)
            else:
                base_date = timezone.datetime(year, base_date.month, base_date.day,
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
            month_last_day = calendar.monthrange(year, month)[1]
            if(base_date.day>month_last_day):
                day = month_last_day
            else:
                day = base_date.day
            if (start_at_midnight == True):
                base_date = timezone.datetime(year, month, day, 0, 0, 0, 0,
                                     base_date.tzinfo)
                
                
            else:
                base_date = timezone.datetime(year, month, day,
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
                base_date = timezone.datetime(year, month, day, 0, 0, 0, 0,
                                     base_date.tzinfo)
            else:
                base_date = timezone.datetime(year, month, day, base_date.hour,
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
        
    @classmethod
    def find_period_list(cls, base_date, event_date, time_unit,  client_status=ClientStatusType.ACTIVE):
        """
        Returns a list of periods for processing, using defaults on a client
        obligation object.
        """
        period_list = []
        from_registration_date = SystemParameter.find_one(
            'OBLIGATION_CALCULATE_PERIODS_FROM_REGISTRATION',
            FieldDataType.BOOLEAN, True)

        # if the client is defunct, it does not make sense to continue
        # calculating anything.
       
        if (client_status == ClientStatusType.DEFUNCT):
            return period_list

        if (event_date is None):
            event_date = timezone.now()
        if (time_unit == TimeUnitType.YEAR):
            number_of_years_into_future = SystemParameter.find_one(
                "OBLIGATION_DEFAULT_NUMBER_OF_YEARS_INTO_FUTURE",
                FieldDataType.INTEGER, 3)
            require_full_years = SystemParameter.find_one(
                "OBLIGATION_CALCULATE_PERIODS_REQUIRE_FULL_YEARS",
                FieldDataType.BOOLEAN, True)
            if (require_full_years == True):
                base_date = base_date + relativedelta(years=1)

            interval = relativedelta(
                event_date, base_date).years + number_of_years_into_future

            for i in range(0, interval):
                period_list.append(int(str(base_date.year).zfill(4)))
                base_date = base_date + relativedelta(years=1)

        elif (time_unit == TimeUnitType.MONTH):
            number_of_months_into_future = SystemParameter.find_one(
                "OBLIGATION_DEFAULT_NUMBER_OF_MONTHS_INTO_FUTURE",
                FieldDataType.INTEGER, 3)
            require_full_months = SystemParameter.find_one(
                "OBLIGATION_CALCULATE_PERIODS_REQUIRE_FULL_MONTHS",
                FieldDataType.BOOLEAN, True)
            if (require_full_months == True):
                base_date = base_date + relativedelta(months=1)

            delta = relativedelta(event_date, base_date)
            interval = delta.years * 12 + delta.months + number_of_months_into_future

            for i in range(0, interval):
                period_list.append(
                    int(
                        str(base_date.year).zfill(4) + str(base_date.month)
                        .zfill(2)))
                base_date = base_date + relativedelta(months=1)

        elif (time_unit == TimeUnitType.DAY):
            number_of_days_into_future = SystemParameter.find_one(
                "OBLIGATION_DEFAULT_NUMBER_OF_DAYS_INTO_FUTURE",
                FieldDataType.INTEGER, 3)

            delta = relativedelta(event_date, base_date)

            interval = delta.years * 12 + delta.months * 30 + delta.days + number_of_days_into_future

            for i in range(0, interval):
                period_list.append(
                    int(
                        str(base_date.year).zfill(4) + str(base_date.month)
                        .zfill(2) + str(base_date.day).zfill(2)))
                base_date = base_date + relativedelta(days=1)
        else:
            raise NotImplementedError

        return period_list
    
    @classmethod
    def find_period_list_by_client_obligation(cls,  client_obligation,  event_date):
        """
        Returns a list of periods for processing, using defaults on a client
        obligation object.
        """
        
        time_unit = TimeUnitType.to_enum(client_obligation.obligation_rule.time_unit_type)
        period_list = []
        from_registration_date = SystemParameter.find_one(
            'OBLIGATION_CALCULATE_PERIODS_FROM_REGISTRATION',
            FieldDataType.BOOLEAN, True)

        # if the client is defunct, it does not make sense to continue
        # calculating anything.
        if (client_obligation.client.status == ClientStatusType.DEFUNCT):
            return period_list

        if (client_obligation.client.registration_date >
                client_obligation.start_date
                and from_registration_date == True):
            base_date = client_obligation.start_date
        else:
            base_date = client_obligation.client.registration_date

        if (event_date is None):
            event_date = timezone.now()
        if (time_unit == TimeUnitType.YEAR):
            number_of_years_into_future = SystemParameter.find_one(
                "OBLIGATION_DEFAULT_NUMBER_OF_YEARS_INTO_FUTURE",
                FieldDataType.INTEGER, 3)
            require_full_years = SystemParameter.find_one(
                "OBLIGATION_CALCULATE_PERIODS_REQUIRE_FULL_YEARS",
                FieldDataType.BOOLEAN, True)
            if (require_full_years == True):
                base_date = base_date + relativedelta(years=1)

            interval = relativedelta(
                event_date, base_date).years + number_of_years_into_future

            for i in range(0, interval):
                period_list.append(int(str(base_date.year).zfill(4)))
                base_date = base_date + relativedelta(years=1)

        elif (time_unit == TimeUnitType.MONTH):
            number_of_months_into_future = SystemParameter.find_one(
                "OBLIGATION_DEFAULT_NUMBER_OF_MONTHS_INTO_FUTURE",
                FieldDataType.INTEGER, 3)
            require_full_months = SystemParameter.find_one(
                "OBLIGATION_CALCULATE_PERIODS_REQUIRE_FULL_MONTHS",
                FieldDataType.BOOLEAN, True)
            if (require_full_months == True):
                base_date = base_date + relativedelta(months=1)

            delta = relativedelta(event_date, base_date)
            interval = delta.years * 12 + delta.months + number_of_months_into_future

            for i in range(0, interval):
                period_list.append(
                    int(
                        str(base_date.year).zfill(4) + str(base_date.month)
                        .zfill(2)))
                base_date = base_date + relativedelta(months=1)

        elif (time_unit == TimeUnitType.DAY):
            number_of_days_into_future = SystemParameter.find_one(
                "OBLIGATION_DEFAULT_NUMBER_OF_DAYS_INTO_FUTURE",
                FieldDataType.INTEGER, 3)

            delta = relativedelta(event_date, base_date)

            interval = delta.years * 12 + delta.months * 30 + delta.days + number_of_days_into_future

            for i in range(0, interval):
                period_list.append(
                    int(
                        str(base_date.year).zfill(4) + str(base_date.month)
                        .zfill(2) + str(base_date.day).zfill(2)))
                base_date = base_date + relativedelta(days=1)
        else:
            raise NotImplementedError

        return period_list
    
    @classmethod
    def find_period_list_by_units(cls, base_date, time_unit, units_before,
                                   units_after):
        """
        Returns a list of periods for processing, with units before and after a
        baseTime
        """
        period_list = []

        if (time_unit == TimeUnitType.YEAR):
            base_date = base_date - relativedelta(years=units_before)
            for i in range(0, units_before + units_after):
                period_list.append(base_date.year)
                base_date = base_date + relativedelta(years=1)
        elif (time_unit == TimeUnitType.MONTH):
            base_date = base_date - relativedelta(months=units_before)
            for i in range(0, units_before + units_after):
                period_list.append(
                    int(str(base_date.year) + str(base_date.month)))
                base_date = base_date + relativedelta(months=1)
        elif (time_unit == TimeUnitType.DAY):
            base_date = base_date - relativedelta(days=units_before)
            for i in range(0, units_before + units_after):
                period_list.append(
                    int(
                        str(base_date.year) + str(base_date.month) +
                        str(base_date.day)))
                base_date = base_date + relativedelta(months=1)
        else:
            raise NotImplementedError

        return period_list
    