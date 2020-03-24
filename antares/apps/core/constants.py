from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class ActionParameterDirectionType(EnumUtilsMixin, models.TextChoices):
    IN = "In", _(__name__ + '.ActionParameterDirectionType.' + 'IN')
    OUT = "Out", _(__name__ + '.ActionParameterDirectionType.' + 'OUT')
    IN_OUT = "In out", _(__name__ + '.ActionParameterDirectionType.' + 'IN_OUT')


class EnvironmentType(EnumUtilsMixin, models.TextChoices):
    LOCAL = "Local", _(__name__ + '.EnvironmentType.' + 'LOCAL')
    WEBSERVICE = "Web Service", _(__name__ + '.EnvironmentType.' + 'WEBSERVICE')


class ActionTargetModuleType(EnumUtilsMixin, models.TextChoices):
    DOCUMENT = "Document", _(__name__ + '.ActionTargetModuleType.' + 'DOCUMENT')
    FLOW = "Flow", _(__name__ + '.ActionTargetModuleType.' + 'FLOW')


class ActionType(EnumUtilsMixin, models.TextChoices):
    PRE_ACTION = "Preaction", _(__name__ + '.ActionType.' + 'PRE_ACTION')
    POST_ACTION = "Postaction", _(__name__ + '.ActionType.' + 'PRE_ACTION')


class FieldDataType(EnumUtilsMixin, models.TextChoices):
    STRING = "String", _(__name__ + '.FieldDataType.STRING')
    TEXT = "Text", _(__name__ + '.FieldDataType.TEXT')
    DATE = "Date", _(__name__ + '.FieldDataType.DATE')
    DATETIME = "Datetime", _(__name__ + '.FieldDataType.DATETIME')
    INTEGER = "Integer", _(__name__ + '.FieldDataType.INTEGER')
    FLOAT = "Float", _(__name__ + '.FieldDataType.FLOAT')
    UUID = "UUID", _(__name__ + '.FieldDataType.UUID')
    BOOLEAN = "Boolean", _(__name__ + '.FieldDataType.BOOLEAN')
    USER = "User", _(__name__ + '.FieldDataType.USER')
    CLIENT = "client", _(__name__ + '.FieldDataType.CLIENT')
    DOCUMENT = "document", _(__name__ + '.FieldDataType.DOCUMENT')
    MONEY = "Money", _(__name__ + '.FieldDataType.MONEY')


class HrnModuleType(EnumUtilsMixin, models.TextChoices):
    DOCUMENT = "Document", _(__name__ + '.HrnModuleType.' + 'DOCUMENT')
    FLOW_CASE = "Flow Case", _(__name__ + '.HrnModuleType.' + 'FLOW_CASE')
    FLOW_ACTIVITY = "Flow Activity", _(__name__ + '.HrnModuleType.' + 'FLOW_ACTIVITY')
    ACCOUNT_BALANCE = "Account Balance", _(__name__ + '.HrnModuleType.' + 'ACCOUNT_BALANCE')
    ACCOUNT_TRANSACTION = "Account Transaction", _(__name__ + '.HrnModuleType.' + 'ACCOUNT_TRANSACTION')


class ScriptEngineType(EnumUtilsMixin, models.TextChoices):
    JAVASCRIPT = "Javascript", _(__name__ + '.ScriptEngineType.' + 'JAVASCRIPT')
    PYTHON = "Python", _(__name__ + '.ScriptEngineType.' + 'PYTHON')


class TimeUnitType(EnumUtilsMixin, models.TextChoices):
    YEAR = "Year", _(__name__ + '.TimeUnitType.' + 'YEAR')
    MONTH = "Month", _(__name__ + '.TimeUnitType.' + 'MONTH')
    DAY = "Day", _(__name__ + '.TimeUnitType.' + 'DAY')
    HOUR = "Hour", _(__name__ + '.TimeUnitType.' + 'HOUR')
    MINUTE = "Minute", _(__name__ + '.TimeUnitType.' + 'MINUTE')
    SECOND = "Second", _(__name__ + '.TimeUnitType.' + 'SECOND')

    @classmethod
    def to_enum_from_xpdl(cls, time_unit):
        """ 
        Converts from xpdl duration units to this type
        """
        if time_unit == 'Y':
            return TimeUnitType.YEAR
        if time_unit == 'M':
            return TimeUnitType.MONTH
        if time_unit == 'D':
            return TimeUnitType.DAY
        if time_unit == 'h':
            return TimeUnitType.HOUR
        if time_unit == 'm':
            return TimeUnitType.MINUTE
        if time_unit == 's':
            return TimeUnitType.SECOND
        else:
            raise ValueError(
                _(__name__ + ".Exceptions.TimeUnitType.Invalid_time_unit"))


class LanguageType(EnumUtilsMixin, models.TextChoices):
    ENGLISH = "en", _(__name__ + '.LanguageType.' + 'ENGLISH')
    SPANISH = "es", _(__name__ + '.LanguageType.' + 'SPANISH')
    FRENCH = "fr", _(__name__ + '.LanguageType.' + 'FRENCH')
    PORTUGUESE = "pr", _(__name__ + '.LanguageType.' + 'PORTUGUESE')


class WeightUnitType(EnumUtilsMixin, models.TextChoices):
    KILOGRAM = "Kilogram", _(__name__ + '.WeightUnitType.' + 'KILOGRAM')
    GRAM = "Gram", _(__name__ + '.WeightUnitType.' + 'GRAM')
    TON = "Ton", _(__name__ + '.WeightUnitType.' + 'TON')


class SystemModuleType(EnumUtilsMixin, models.TextChoices):
    ACCOUNTING = "Accounting", _(__name__ + '.SystemModuleType.' + 'ACCOUNTING')
    CLIENT = "Client", _(__name__ + '.SystemModuleType.' + 'CLIENT')
    CORE = "Core", _(__name__ + '.SystemModuleType.' + 'CORE')
    DOCUMENT = "Document", _(__name__ + '.SystemModuleType.' + 'DOCUMENT')
    FLOW = "Flow", _(__name__ + '.SystemModuleType.' + 'FLOW')
    NOTIFICATIONS = "Notifications", _(__name__ + '.SystemModuleType.' + 'NOTIFICATIONS')
    OBLIGATION = "Obligation", _(__name__ + '.SystemModuleType.' + 'OBLIGATION')
    SUBSCRIPTION = "Subscription", _(__name__ + '.SystemModuleType.' + 'SUBSCRIPTION')
    TERMINAL = "Terminal", _(__name__ + '.SystemModuleType.' + 'TERMINAL')
    MESSAGE = 'Message', _(__name__ + '.SystemModuleType.' + 'MESSAGE')
    THIRD_PARTY = "Third Party", _(__name__ + '.SystemModuleType.' + 'THIRD_PARTY')
    WEB = "Web", _(__name__ + '.SystemModuleType.' + 'WEB')
