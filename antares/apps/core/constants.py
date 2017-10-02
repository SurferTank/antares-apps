from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class ActionParameterDirectionType(EnumUtilsMixin, Enum):
    IN = "In"
    OUT = "Out"
    IN_OUT = "In out"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        IN = _(__name__ + '.ActionParameterDirectionType.' + 'IN')
        OUT = _(__name__ + '.ActionParameterDirectionType.' + 'OUT')
        IN_OUT = _(__name__ + '.ActionParameterDirectionType.' + 'IN_OUT')


class EnvironmentType(EnumUtilsMixin, Enum):
    LOCAL = "Local"
    WEBSERVICE = "Web Service"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        LOCAL = _(__name__ + '.EnvironmentType.' + 'LOCAL')
        WEBSERVICE = _(__name__ + '.EnvironmentType.' + 'WEBSERVICE')


class ActionTargetModuleType(EnumUtilsMixin, Enum):
    DOCUMENT = "Document"
    FLOW = "Flow"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        DOCUMENT = _(__name__ + '.ActionTargetModuleType.' + 'DOCUMENT')
        FLOW = _(__name__ + '.ActionTargetModuleType.' + 'FLOW')


class ActionType(EnumUtilsMixin, Enum):
    PRE_ACTION = "Preaction"
    POST_ACTION = "Postaction"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        PRE_ACTION = _(__name__ + '.ActionType.' + 'PRE_ACTION')
        POST_ACTION = _(__name__ + '.ActionType.' + 'PRE_ACTION')


class FieldDataType(EnumUtilsMixin, Enum):
    STRING = "String"
    TEXT = "Text"
    DATE = "Date"
    DATETIME = "Datetime"
    INTEGER = "Integer"
    FLOAT = "Float"
    UUID = "UUID"
    BOOLEAN = "Boolean"
    USER = "User"
    CLIENT = "client"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        STRING = _(__name__ + '.FieldDataType.' + 'STRING')
        TEXT = _(__name__ + '.FieldDataType.' + 'TEXT')
        DATE = _(__name__ + '.FieldDataType.' + 'DATE')
        DATETIME =  _(__name__ + '.FieldDataType.' + 'DATETIME')
        INTEGER = _(__name__ + '.FieldDataType.' + 'INTEGER')
        FLOAT = _(__name__ + '.FieldDataType.' + 'FLOAT')
        UUID = _(__name__ + '.FieldDataType.' + 'UUID')
        BOOLEAN = _(__name__ + '.FieldDataType.' + 'BOOLEAN')
        USER = _(__name__ + '.FieldDataType.' + 'USER')
        CLIENT = _(__name__ + '.FieldDataType.' + 'CLIENT')
        

class HrnModuleType(EnumUtilsMixin, Enum):
    DOCUMENT = "Document"
    FLOW_CASE = "Flow Case"
    FLOW_ACTIVITY = "Flow Activity"
    ACCOUNT_BALANCE = "Account Balance"
    ACCOUNT_TRANSACTION = "Account Transaction"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        DOCUMENT = _(__name__ + '.HrnModuleType.' + 'DOCUMENT')
        FLOW_CASE = _(__name__ + '.HrnModuleType.' + 'FLOW_CASE')
        FLOW_ACTIVITY = _(__name__ + '.HrnModuleType.' + 'FLOW_ACTIVITY')
        ACCOUNT_BALANCE = _(__name__ + '.HrnModuleType.' + 'ACCOUNT_BALANCE')
        ACCOUNT_TRANSACTION = _(__name__ + '.HrnModuleType.' +
                                'ACCOUNT_BALANCE')


class ScriptEngineType(EnumUtilsMixin, Enum):
    JAVASCRIPT = "Javascript"
    PYTHON = "Python"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        JAVASCRIPT = _(__name__ + '.ScriptEngineType.' + 'JAVASCRIPT')
        PYTHON = _(__name__ + '.ScriptEngineType.' + 'PYTHON')


class TimeUnitType(EnumUtilsMixin, Enum):
    YEAR = "Year"
    MONTH = "Month"
    DAY = "Day"
    HOUR = "Hour"
    MINUTE = "Minute"
    SECOND = "Second"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

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

    class Labels:
        YEAR = _(__name__ + '.TimeUnitType.' + 'YEAR')
        MONTH = _(__name__ + '.TimeUnitType.' + 'MONTH')
        DAY = _(__name__ + '.TimeUnitType.' + 'DAY')
        HOUR = _(__name__ + '.TimeUnitType.' + 'HOUR')
        MINUTE = _(__name__ + '.TimeUnitType.' + 'MINUTE')
        SECOND = _(__name__ + '.TimeUnitType.' + 'SECOND')


class LanguageType(EnumUtilsMixin, Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    PORTUGUESE = "pr"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ENGLISH = _(__name__ + '.LanguageType.' + 'ENGLISH')
        SPANISH = _(__name__ + '.LanguageType.' + 'SPANISH')
        FRENCH = _(__name__ + '.LanguageType.' + 'FRENCH')
        PORTUGUESE = _(__name__ + '.LanguageType.' + 'PORTUGUESE')


class WeightUnitType(EnumUtilsMixin, Enum):
    KILOGRAM = "Kilogram"
    GRAM = "Gram"
    TON = "Ton"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        KILOGRAM = _(__name__ + '.WeightUnitType.' + 'KILOGRAM')
        GRAM = _(__name__ + '.WeightUnitType.' + 'GRAM')
        TON = _(__name__ + '.WeightUnitType.' + 'TON')


class SystemModuleType(EnumUtilsMixin, Enum):
    ACCOUNTING = "Accounting"
    CLIENT = "Client"
    CORE = "Core"
    DOCUMENT = "Document"
    FLOW = "Flow"
    NOTIFICATIONS = "Notifications"
    OBLIGATION = "Obligation"
    SUBSCRIPTION = "Subscription"
    TERMINAL = "Terminal"
    MESSAGE = 'Message'
    THIRD_PARTY = "Third Party"
    WEB = "Web"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ACCOUNTING = _(__name__ + '.SystemModuleType.' + 'ACCOUNTING')
        CLIENT = _(__name__ + '.SystemModuleType.' + 'CLIENT')
        CORE = _(__name__ + '.SystemModuleType.' + 'CORE')
        DOCUMENT = _(__name__ + '.SystemModuleType.' + 'DOCUMENT')
        FLOW = _(__name__ + '.SystemModuleType.' + 'FLOW')
        NOTIFICATIONS = _(__name__ + '.SystemModuleType.' + 'NOTIFICATIONS')
        OBLIGATION = _(__name__ + '.SystemModuleType.' + 'OBLIGATION')
        SUBSCRIPTION = _(__name__ + '.SystemModuleType.' + 'SUBSCRIPTION')
        TERMINAL = _(__name__ + '.SystemModuleType.' + 'TERMINAL')
        MESSAGE = _(__name__ + '.SystemModuleType.' + 'MESSAGE')
        THIRD_PARTY = _(__name__ + '.SystemModuleType.' + 'THIRD_PARTY')
        WEB = _(__name__ + '.SystemModuleType.' + 'WEB')
