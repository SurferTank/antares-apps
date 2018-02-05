'''
Created on Jun 23, 2016

@author: leobelen
'''
from enumfields import Enum
from antares.apps.core.mixins import EnumUtilsMixin

from django.utils.translation import ugettext as _


class DocumentAssociationType(EnumUtilsMixin, Enum):
    NONE = "None"

    class Labels:
        NONE = _(__name__ + '.DocumentAssociationType.' + 'NONE')


class DocumentEventType(EnumUtilsMixin, Enum):
    CREATION = "Creation"
    DRAFT_MODIFICATION = "Draft Modification"
    SAVE = "Save"
    CANCELLATION = "Cancellation"

    class Labels:
        CREATION = _(__name__ + '.DocumentEventType.' + 'CREATION')
        DRAFT_MODIFICATION = _(
            __name__ + '.DocumentEventType.' + 'DRAFT_MODIFICATION')
        SAVE = _(__name__ + '.DocumentEventType.' + 'SAVE')
        CANCELLATION = _(__name__ + '.DocumentEventType.' + 'CANCELLATION')


class DocumentACLAccessType(EnumUtilsMixin, Enum):
    CREATE = "Create"
    MODIFY = "Modify"
    SAVE = "Save"
    CANCEL = "Cancel"
    VIEW = "View"
    PRINT = "Print"
    ALL = "ALL"
    NONE = "None"

    class Labels:
        CREATE = _(__name__ + '.DocumentACLAcessType.' + 'CREATE')
        MODIFY = _(__name__ + '.DocumentACLAcessType.' + 'MODIFY')
        SAVE = _(__name__ + '.DocumentACLAcessType.' + 'SAVE')
        CANCEL = _(__name__ + '.DocumentACLAcessType.' + 'CANCEL')
        VIEW = _(__name__ + '.DocumentACLAcessType.' + 'VIEW')
        PRINT = _(__name__ + '.DocumentACLAcessType.' + 'PRINT')
        ALL = _(__name__ + '.DocumentACLAcessType.' + 'ALL')
        NONE = _(__name__ + '.DocumentACLAcessType.' + 'NONE')


class FormDefinitionACLAccessType(EnumUtilsMixin, Enum):
    CREATE = "Create"
    SEARCH = "Search"
    ALL = "ALL"
    NONE = "None"

    class Labels:
        CREATE = _(__name__ + '.FormDefinitionACLAccessType.' + 'CREATE')
        SEARCH = _(__name__ + '.FormDefinitionACLAccessType.' + 'SEARCH')
        ALL = _(__name__ + '.FormDefinitionACLAccessType.' + 'ALL')
        NONE = _(__name__ + '.FormDefinitionACLAccessType.' + 'NONE')


class DocumentOriginType(EnumUtilsMixin, Enum):
    ONLINE = "Online"
    UNKNOWN = "Unknown"

    class Labels:
        ONLINE = _(__name__ + '.DocumentOriginType.' + 'ONLINE')
        UNKNOWN = _(__name__ + '.DocumentOriginType.' + 'UNKNOWN')


class DocumentStatusType(EnumUtilsMixin, Enum):
    DRAFTED = "Drafted"
    DELETED = "Deleted"
    SAVED = "Saved"
    CANCELLED = "Cancelled"

    class Labels:
        DRAFTED = _(__name__ + '.DocumentStatusType.' + 'DRAFTED')
        DELETED = _(__name__ + '.DocumentStatusType.' + 'DELETED')
        SAVED = _(__name__ + '.DocumentStatusType.' + 'SAVED')
        CANCELLED = _(__name__ + '.DocumentStatusType.' + 'CANCELLED')


class ExternalFunctionExecutionModeType(EnumUtilsMixin, Enum):
    DRAFT_LOAD = "DRAFT_LOAD"
    CREATION_TIME = "CREATION_TIME"
    RUNTIME = "RUNTIME"
    INACTIVE = "INACTIVE"
    SAVE_TIME = "SAVE_TIME"

    class Labels:
        DRAFT_LOAD = _(
            __name__ + '.ExternalFunctionExecutionModeType.' + 'DRAFT_LOAD')
        CREATION_TIME = _(
            __name__ + '.ExternalFunctionExecutionModeType.' + 'CREATION_TIME')
        RUNTIME = _(
            __name__ + '.ExternalFunctionExecutionModeType.' + 'RUNTIME')
        INACTIVE = _(
            __name__ + '.ExternalFunctionExecutionModeType.' + 'INACTIVE')
        SAVE_TIME = _(
            __name__ + '.ExternalFunctionExecutionModeType.' + 'SAVE_TIME')


class FormClassStatusType(EnumUtilsMixin, Enum):
    DEVELOPMENT = "Development"
    PRODUCTION = "Production"
    DEACTIVATED = "Deactivated"

    class Labels:
        DEVELOPMENT = _(__name__ + '.FormClassStatusType.' + 'DEVELOPMENT')
        PRODUCTION = _(__name__ + '.FormClassStatusType.' + 'PRODUCTION')
        DEACTIVATED = _(__name__ + '.FormClassStatusType.' + 'DEACTIVATED')


class FormDefinitionStatusType(EnumUtilsMixin, Enum):
    DEVELOPMENT = "Development"
    PRODUCTION = "Production"
    DEACTIVATED = "Deactivated"

    class Labels:
        DEVELOPMENT = _(
            __name__ + '.FormDefinitionStatusType.' + 'DEVELOPMENT')
        PRODUCTION = _(__name__ + '.FormDefinitionStatusType.' + 'PRODUCTION')
        DEACTIVATED = _(
            __name__ + '.FormDefinitionStatusType.' + 'DEACTIVATED')


class FormClassType(EnumUtilsMixin, Enum):
    ADMINISTRATIVE = "Administrative"
    OBLIGATION_BASED = "Obligation Based"

    class Labels:
        ADMINISTRATIVE = _(__name__ + '.FormClassType.' + 'ADMINISTRATIVE')
        OBLIGATION_BASED = _(__name__ + '.FormClassType.' + 'OBLIGATION_BASED')
