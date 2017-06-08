'''
Created on Jul 9, 2016

@author: leobelen
'''
from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class ActivityApplicationDefinitionScopeType(EnumUtilsMixin, Enum):
    SAME = "Same"
    BLANK = "Blank"
    DIALOG = 'Dialog'

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Label:
        SAME = _(__name__ + 'ActivityApplicationDefinitionScopeType.' + 'SAME')
        BLANK = _(__name__ + 'ActivityApplicationDefinitionScopeType.' +
                  'BLANK')
        DIALOG = _(__name__ + 'ActivityApplicationDefinitionScopeType.' +
                   'DIALOG')


class ActivityType(EnumUtilsMixin, Enum):
    ROUTE = "Route"
    TASK = "Task"
    NO_IMPLEMENTATION = "No Implementation"
    SUBFLOW = "Sub Flow"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ROUTE = _(__name__ + '.ActivityType.' + 'ROUTE')
        TASK = _(__name__ + '.ActivityType.' + 'TASK')
        NO_IMPLEMENTATION = _(__name__ + '.ActivityType.' +
                              'NO_IMPLEMENTATION')
        SUBFLOW = _(__name__ + '.ActivityType.' + 'SUBFLOW')


class AssignmentStrategyType(EnumUtilsMixin, Enum):
    DIRTY_RANDOM = "Dirty Random"
    RANDOM = "Random"
    PROPERTY = "Property"
    ACTIVITY = "Activity"
    WORKLOAD = "Workload"
    NONE = "None"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        DIRTY_RANDOM = _(__name__ + '.AssignmentStrategyType.' +
                         'DIRTY_RANDOM')
        RANDOM = _(__name__ + '.AssignmentStrategyType.' + 'RANDOM')
        PROPERTY = _(__name__ + '.AssignmentStrategyType.' + 'PROPERTY')
        ACTIVITY = _(__name__ + '.AssignmentStrategyType.' + 'ACTIVITY')
        WORKLOAD = _(__name__ + '.AssignmentStrategyType.' + 'WORKLOAD')
        NONE = _(__name__ + '.AssignmentStrategyType.' + 'NONE')


class DefinitionSiteType(EnumUtilsMixin, Enum):
    PACKAGE = "Package"
    FLOW = "Flow"
    SYSTEM = "System"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        PACKAGE = _(__name__ + '.DefinitionSiteType.' + 'PACKAGE')
        FLOW = _(__name__ + '.DefinitionSiteType.' + 'FLOW')
        SYSTEM = _(__name__ + '.DefinitionSiteType.' + 'SYSTEM')


class ExecutionModeType(EnumUtilsMixin, Enum):
    AUTOMATIC = "Automatic"
    MANUAL = "Manual"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        AUTOMATIC = _(__name__ + '.ExecutionModeType.' + 'AUTOMATIC')
        MANUAL = _(__name__ + '.ExecutionModeType.' + 'MANUAL')


class FlowAccessLevelType(EnumUtilsMixin, Enum):
    PRIVATE_MODE = "Private"
    PUBLIC_MODE = "Public"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        PRIVATE_MODE = _(__name__ + '.FlowAccessLevelType.' + 'PRIVATE_MODE')
        PUBLIC_MODE = _(__name__ + '.FlowAccessLevelType.' + 'PUBLIC_MODE')


class FlowActivityStatusType(EnumUtilsMixin, Enum):
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    ACTIVE = "Active"
    CREATED = "Created"
    REASSIGNED = "Reassigned"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        COMPLETED = _(__name__ + '.FlowActivityStatusType.' + 'COMPLETED')
        CANCELLED = _(__name__ + '.FlowActivityStatusType.' + 'CANCELLED')
        ACTIVE = _(__name__ + '.FlowActivityStatusType.' + 'ACTIVE')
        CREATED = _(__name__ + '.FlowActivityStatusType.' + 'CREATED')
        REASSIGNED = _(__name__ + '.FlowActivityStatusType.' + 'REASSIGNED')


class FlowBasicDataSubtype(EnumUtilsMixin, Enum):
    STRING = "String"
    TEXT = "Text"
    DATE = "Date"
    INTEGER = "Integer"
    FLOAT = "Float"
    BOOLEAN = "Boolean"
    REFERENCE = "Reference"
    PERFORMER = "Performer"
    UUID = "UUID"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        STRING = _(__name__ + '.FlowBasicDataSubtype.' + 'STRING')
        TEXT = _(__name__ + '.FlowBasicDataSubtype.' + 'TEXT')
        DATE = _(__name__ + '.FlowBasicDataSubtype.' + 'DATE')
        INTEGER = _(__name__ + '.FlowBasicDataSubtype.' + 'INTEGER')
        FLOAT = _(__name__ + '.FlowBasicDataSubtype.' + 'FLOAT')
        BOOLEAN = _(__name__ + '.FlowBasicDataSubtype.' + 'BOOLEAN')
        REFERENCE = _(__name__ + '.FlowBasicDataSubtype.' + 'REFERENCE')
        PERFORMER = _(__name__ + '.FlowBasicDataSubtype.' + 'PERFORMER')
        UUID = _(__name__ + '.FlowBasicDataSubtype.' + 'UUID')


class FlowCaseSourceType(EnumUtilsMixin, Enum):
    DOCUMENT = "Document"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        DOCUMENT = _(__name__ + '.FlowCaseSourceType.' + 'DOCUMENT')


class FlowCaseStatusType(EnumUtilsMixin, Enum):
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    ACTIVE = "Active"
    CREATED = "Created"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        COMPLETED = _(__name__ + '.FlowCaseStatusType.' + 'COMPLETED')
        CANCELLED = _(__name__ + '.FlowCaseStatusType.' + 'CANCELLED')
        ACTIVE = _(__name__ + '.FlowCaseStatusType.' + 'ACTIVE')
        CREATED = _(__name__ + '.FlowCaseStatusType.' + 'CREATED')


class FlowDataType(EnumUtilsMixin, Enum):
    BASIC = "Basic"
    ENUMERATION = "Enumeration"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        BASIC = _(__name__ + '.FlowDataType.' + 'BASIC')
        ENUMERATION = _(__name__ + '.FlowDataType.' + 'ENUMERATION')


class FlowDefinitionStatusType(EnumUtilsMixin, Enum):
    CREATED = "CREATED"
    UNDER_TEST = "UNDER_TEST"
    UNDER_REVISION = "UNDER_REVISION"
    RELEASED = "RELEASED"
    PHASED_OUT = "PHASED_OUT"
    CANCELLED = "CANCELLED"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        CREATED = _(__name__ + '.FlowDefinitionStatusType.' + 'CREATED')
        UNDER_TEST = _(__name__ + '.FlowDefinitionStatusType.' + 'UNDER_TEST')
        UNDER_REVISION = _(__name__ + '.FlowDefinitionStatusType.' +
                           'UNDER_REVISION')
        RELEASED = _(__name__ + '.FlowDefinitionStatusType.' + 'RELEASED')
        PHASED_OUT = _(__name__ + '.FlowDefinitionStatusType.' + 'PHASED_OUT')
        CANCELLED = _(__name__ + '.FlowDefinitionStatusType.' + 'CANCELLED')


class FlowDocumentRelationshipType(EnumUtilsMixin, Enum):
    ATTACHED = "Attached"
    SOURCE = "Source"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ATTACHED = _(__name__ + '.FlowDocumentRelationshipType.' + 'ATTACHED')
        SOURCE = _(__name__ + '.FlowDocumentRelationshipType.' + 'SOURCE')


class FlowPriorityType(EnumUtilsMixin, Enum):
    TOP = "Top"
    HIGH = "High"
    STANDARD = "Standard"
    LOW = "Low"
    MINIMAL = "Minimal"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        TOP = _(__name__ + '.FlowPriorityType.' + 'TOP')
        HIGH = _(__name__ + '.FlowPriorityType.' + 'HIGH')
        STANDARD = _(__name__ + '.FlowPriorityType.' + 'STANDARD')
        LOW = _(__name__ + '.FlowPriorityType.' + 'LOW')
        MINIMAL = _(__name__ + '.FlowPriorityType.' + 'MINIMAL')


class FormalParameterModeType(EnumUtilsMixin, Enum):
    IN = "IN"
    OUT = "OUT"
    IN_OUT = "IN_OUT"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        IN = _(__name__ + '.FormalParameterModeType.' + 'IN')
        OUT = _(__name__ + '.FormalParameterModeType.' + 'OUT')
        IN_OUT = _(__name__ + '.FormalParameterModeType.' + 'IN_OUT')


class ParticipantType(EnumUtilsMixin, Enum):
    ROLE = "ROLE"
    RESOURCE_SET = "RESOURCE_SET"
    HUMAN = "HUMAN"
    RESOURCE = "RESOURCE"
    ORGANIZATIONAL_UNIT = "ORGANIZATIONAL_UNIT"
    SYSTEM = "SYSTEM"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ROLE = _(__name__ + '.ParticipantType.' + 'ROLE')
        RESOURCE_SET = _(__name__ + '.ParticipantType.' + 'RESOURCE_SET')
        HUMAN = _(__name__ + '.ParticipantType.' + 'HUMAN')
        RESOURCE = _(__name__ + '.ParticipantType.' + 'RESOURCE')
        ORGANIZATIONAL_UNIT = _(__name__ + '.ParticipantType.' +
                                'ORGANIZATIONAL_UNIT')
        SYSTEM = _(__name__ + '.ParticipantType.' + 'SYSTEM')


class PropertyType(EnumUtilsMixin, Enum):
    DATA_FIELD = "Data Field"
    FORMAL_PARAMETER = "Formal Parameter"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        DATA_FIELD = _(__name__ + '.PropertyType.' + 'DATA_FIELD')
        FORMAL_PARAMETER = _(__name__ + '.PropertyType.' + 'FORMAL_PARAMETER')


class TransitionType(EnumUtilsMixin, Enum):
    CONDITION = "CONDITION"
    DEFAULT_EXCEPTION = "DEFAULT_EXCEPTION"
    EXCEPTION = "EXCEPTION"
    OTHERWISE = "OTHERWISE"
    NONE = "NONE"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        CONDITION = _(__name__ + '.TransitionType.' + 'CONDITION')
        DEFAULT_EXCEPTION = _(__name__ + '.TransitionType.' +
                              'DEFAULT_EXCEPTION')
        EXCEPTION = _(__name__ + '.TransitionType.' + 'EXCEPTION')
        OTHERWISE = _(__name__ + '.TransitionType.' + 'OTHERWISE')
        NONE = _(__name__ + '.TransitionType.' + 'NONE')


class FlowDefinitionAccessLevelType(EnumUtilsMixin, Enum):
    PRIVATE = "Private"
    PUBLIC = "Public"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        PRIVATE = _(__name__ + '.FlowDefinitionAccessLevelType.' + 'PRIVATE')
        PUBLIC = _(__name__ + '.FlowDefinitionAccessLevelType.' + 'PUBLIC')


class FlowActivityInstantiationType(EnumUtilsMixin, Enum):
    ONCE = "Once"
    MULTIPLE = "Multiple"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ONCE = _(__name__ + '.FlowActivityInstantiationType.' + 'ONCE')
        MULTIPLE = _(__name__ + '.FlowActivityInstantiationType.' + 'MULTIPLE')


class TimeEstimationMethodType(EnumUtilsMixin, Enum):
    AVERAGE = "Average"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        AVERAGE = _(__name__ + '.TimeEstimationMethodType.' + 'AVERAGE')
