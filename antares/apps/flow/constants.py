'''
Created on Jul 9, 2016

@author: leobelen
'''
from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class ActivityApplicationDefinitionScopeType(EnumUtilsMixin, models.TextChoices):
    SAME = "Same", _(__name__ + 'ActivityApplicationDefinitionScopeType.' + 'SAME')
    BLANK = "Blank", _(__name__ + 'ActivityApplicationDefinitionScopeType.' + 
                  'BLANK')
    DIALOG = 'Dialog', _(__name__ + 'ActivityApplicationDefinitionScopeType.' + 
                   'DIALOG')


class ActivityType(EnumUtilsMixin, models.TextChoices):
    ROUTE = "Route", _(__name__ + '.ActivityType.' + 'ROUTE')
    TASK = "Task", _(__name__ + '.ActivityType.' + 'TASK')
    NO_IMPLEMENTATION = "No Implementation", _(__name__ + '.ActivityType.' + 
                              'NO_IMPLEMENTATION')
    SUBFLOW = "Sub Flow", _(__name__ + '.ActivityType.' + 'SUBFLOW')


class AssignmentStrategyType(EnumUtilsMixin, models.TextChoices):
    DIRTY_RANDOM = "Dirty Random", _(__name__ + '.AssignmentStrategyType.' + 
                         'DIRTY_RANDOM')
    RANDOM = "Random", _(__name__ + '.AssignmentStrategyType.' + 'RANDOM')
    PROPERTY = "Property", _(__name__ + '.AssignmentStrategyType.' + 'PROPERTY')
    ACTIVITY = "Activity", _(__name__ + '.AssignmentStrategyType.' + 'ACTIVITY')
    WORKLOAD = "Workload", _(__name__ + '.AssignmentStrategyType.' + 'WORKLOAD')
    NONE = "None", _(__name__ + '.AssignmentStrategyType.' + 'NONE')


class DefinitionSiteType(EnumUtilsMixin, models.TextChoices):
    PACKAGE = "Package", _(__name__ + '.DefinitionSiteType.' + 'PACKAGE')
    FLOW = "Flow", _(__name__ + '.DefinitionSiteType.' + 'FLOW')
    SYSTEM = "System", _(__name__ + '.DefinitionSiteType.' + 'SYSTEM')


class ExecutionModeType(EnumUtilsMixin, models.TextChoices):
    AUTOMATIC = "Automatic", _(__name__ + '.ExecutionModeType.' + 'AUTOMATIC')
    MANUAL = "Manual", _(__name__ + '.ExecutionModeType.' + 'MANUAL')


class FlowAccessLevelType(EnumUtilsMixin, models.TextChoices):
    PRIVATE_MODE = "Private", _(__name__ + '.FlowAccessLevelType.' + 'PRIVATE_MODE')
    PUBLIC_MODE = "Public", _(__name__ + '.FlowAccessLevelType.' + 'PUBLIC_MODE')


class FlowActivityStatusType(EnumUtilsMixin, models.TextChoices):
    COMPLETED = "Completed", _(__name__ + '.FlowActivityStatusType.' + 'COMPLETED')
    CANCELLED = "Cancelled", _(__name__ + '.FlowActivityStatusType.' + 'CANCELLED')
    ACTIVE = "Active", _(__name__ + '.FlowActivityStatusType.' + 'ACTIVE')
    CREATED = "Created", _(__name__ + '.FlowActivityStatusType.' + 'CREATED')
    REASSIGNED = "Reassigned", _(__name__ + '.FlowActivityStatusType.' + 'REASSIGNED')


class FlowBasicDataSubtype(EnumUtilsMixin, models.TextChoices):
    STRING = "String", _(__name__ + '.FlowBasicDataSubtype.' + 'STRING')
    TEXT = "Text", _(__name__ + '.FlowBasicDataSubtype.' + 'TEXT')
    DATE = "Date", _(__name__ + '.FlowBasicDataSubtype.' + 'DATE')
    INTEGER = "Integer", _(__name__ + '.FlowBasicDataSubtype.' + 'INTEGER')
    FLOAT = "Float", _(__name__ + '.FlowBasicDataSubtype.' + 'FLOAT')
    BOOLEAN = "Boolean", _(__name__ + '.FlowBasicDataSubtype.' + 'BOOLEAN')
    REFERENCE = "Reference", _(__name__ + '.FlowBasicDataSubtype.' + 'REFERENCE')
    PERFORMER = "Performer", _(__name__ + '.FlowBasicDataSubtype.' + 'PERFORMER')
    UUID = "UUID", _(__name__ + '.FlowBasicDataSubtype.' + 'UUID')


class FlowCaseSourceType(EnumUtilsMixin, models.TextChoices):
    DOCUMENT = "Document", _(__name__ + '.FlowCaseSourceType.' + 'DOCUMENT')


class FlowCaseStatusType(EnumUtilsMixin, models.TextChoices):
    COMPLETED = "Completed", _(__name__ + '.FlowCaseStatusType.' + 'COMPLETED')
    CANCELLED = "Cancelled", _(__name__ + '.FlowCaseStatusType.' + 'CANCELLED')
    ACTIVE = "Active", _(__name__ + '.FlowCaseStatusType.' + 'ACTIVE')
    CREATED = "Created" , _(__name__ + '.FlowCaseStatusType.' + 'CREATED')


class FlowDataType(EnumUtilsMixin, models.TextChoices):
    BASIC = "Basic", _(__name__ + '.FlowDataType.' + 'BASIC')
    ENUMERATION = "Enumeration", _(__name__ + '.FlowDataType.' + 'ENUMERATION')


class FlowDefinitionStatusType(EnumUtilsMixin, models.TextChoices):
    CREATED = "CREATED", _(__name__ + '.FlowDefinitionStatusType.' + 'CREATED')
    UNDER_TEST = "UNDER_TEST", _(__name__ + '.FlowDefinitionStatusType.' + 'UNDER_TEST')
    UNDER_REVISION = "UNDER_REVISION", _(__name__ + '.FlowDefinitionStatusType.' + 
                           'UNDER_REVISION')
    RELEASED = "RELEASED", _(__name__ + '.FlowDefinitionStatusType.' + 'RELEASED')
    PHASED_OUT = "PHASED_OUT", _(__name__ + '.FlowDefinitionStatusType.' + 'PHASED_OUT')
    CANCELLED = "CANCELLED", _(__name__ + '.FlowDefinitionStatusType.' + 'CANCELLED')


class FlowDocumentRelationshipType(EnumUtilsMixin, models.TextChoices):
    ATTACHED = "Attached", _(__name__ + '.FlowDocumentRelationshipType.' + 'ATTACHED')
    SOURCE = "Source", _(__name__ + '.FlowDocumentRelationshipType.' + 'SOURCE')


class FlowPriorityType(EnumUtilsMixin, models.TextChoices):
    TOP = "Top", _(__name__ + '.FlowPriorityType.' + 'TOP')
    HIGH = "High", _(__name__ + '.FlowPriorityType.' + 'HIGH')
    STANDARD = "Standard", _(__name__ + '.FlowPriorityType.' + 'STANDARD')
    LOW = "Low", _(__name__ + '.FlowPriorityType.' + 'LOW')
    MINIMAL = "Minimal", _(__name__ + '.FlowPriorityType.' + 'MINIMAL')


class FormalParameterModeType(EnumUtilsMixin, models.TextChoices):
    IN = "IN", _(__name__ + '.FormalParameterModeType.' + 'IN')
    OUT = "OUT", _(__name__ + '.FormalParameterModeType.' + 'OUT')
    IN_OUT = "IN_OUT", _(__name__ + '.FormalParameterModeType.' + 'IN_OUT')


class ParticipantType(EnumUtilsMixin, models.TextChoices):
    ROLE = "ROLE", _(__name__ + '.ParticipantType.' + 'ROLE')
    RESOURCE_SET = "RESOURCE_SET", _(__name__ + '.ParticipantType.' + 'RESOURCE_SET')
    HUMAN = "HUMAN", _(__name__ + '.ParticipantType.' + 'HUMAN')
    RESOURCE = "RESOURCE", _(__name__ + '.ParticipantType.' + 'RESOURCE')
    ORGANIZATIONAL_UNIT = "ORGANIZATIONAL_UNIT", _(__name__ + '.ParticipantType.' + 
                                'ORGANIZATIONAL_UNIT')
    SYSTEM = "SYSTEM", _(__name__ + '.ParticipantType.' + 'SYSTEM')


class PropertyType(EnumUtilsMixin, models.TextChoices):
    DATA_FIELD = "Data Field", _(__name__ + '.PropertyType.' + 'DATA_FIELD')
    FORMAL_PARAMETER = "Formal Parameter", _(__name__ + '.PropertyType.' + 'FORMAL_PARAMETER')


class TransitionType(EnumUtilsMixin, models.TextChoices):
    CONDITION = "CONDITION", _(__name__ + '.TransitionType.' + 'CONDITION')
    DEFAULT_EXCEPTION = "DEFAULT_EXCEPTION", _(__name__ + '.TransitionType.' + 
                              'DEFAULT_EXCEPTION')
    EXCEPTION = "EXCEPTION", _(__name__ + '.TransitionType.' + 'EXCEPTION')
    OTHERWISE = "OTHERWISE", _(__name__ + '.TransitionType.' + 'OTHERWISE')
    NONE = "NONE", _(__name__ + '.TransitionType.' + 'NONE')


class FlowDefinitionAccessLevelType(EnumUtilsMixin, models.TextChoices):
    PRIVATE = "Private", _(__name__ + '.FlowDefinitionAccessLevelType.' + 'PRIVATE')
    PUBLIC = "Public", _(__name__ + '.FlowDefinitionAccessLevelType.' + 'PUBLIC')


class FlowActivityInstantiationType(EnumUtilsMixin, models.TextChoices):
    ONCE = "Once", _(__name__ + '.FlowActivityInstantiationType.' + 'ONCE')
    MULTIPLE = "Multiple", _(__name__ + '.FlowActivityInstantiationType.' + 'MULTIPLE')


class TimeEstimationMethodType(EnumUtilsMixin, models.TextChoices):
    AVERAGE = "Average", _(__name__ + '.TimeEstimationMethodType.' + 'AVERAGE')

