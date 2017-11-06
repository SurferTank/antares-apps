class DateUtils(object):
    @classmethod
    def convert_days_to_time_unit(cls, days, time_unit=None):
        """ 
        Converts an amount of days to the specified time unit, as the ORM returns differences in days.
        """
        from ..models import SystemParameter
        from ..constants import TimeUnitType, FieldDataType
        from django.utils.translation import ugettext as _

        if isinstance(str, time_unit):
            time_unit = TimeUnitType.to_enum(time_unit)

        if time_unit is None:
            time_unit = TimeUnitType.to_enum(
                SystemParameter.find_one("DEFAULT_TIME_UNIT",
                                         FieldDataType.STRING,
                                         TimeUnitType.HOUR.value))

        if time_unit == TimeUnitType.YEAR:
            return days / 365
        if time_unit == TimeUnitType.MONTH:
            return days / 30
        if time_unit == TimeUnitType.DAY:
            return days
        if time_unit == TimeUnitType.HOUR:
            return days * 24
        if time_unit == TimeUnitType.MINUTE:
            return days * 24 * 60
        if time_unit == TimeUnitType.SECOND:
            return days * 24 * 60 * 60
        raise ValueError(_(__name__ + ".exceptions.invalid_time_unit"))
