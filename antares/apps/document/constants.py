'''
Created on Jun 23, 2016

@author: leobelen
'''
from django.utils.translation import ugettext as _
from django.db import models

from antares.apps.core.mixins import EnumUtilsMixin


class DocumentAssociationType(EnumUtilsMixin, models.TextChoices):
    NONE = "None", _(__name__ + '.DocumentAssociationType.' + 'NONE')


class DocumentEventType(EnumUtilsMixin, models.TextChoices):
    CREATION = "Creation", _(__name__ + '.DocumentEventType.' + 'CREATION')
    DRAFT_MODIFICATION = "Draft Modification", _(__name__ + '.DocumentEventType.' +
                               'DRAFT_MODIFICATION')
    SAVE = "Save", _(__name__ + '.DocumentEventType.' + 'SAVE')
    CANCELLATION = "Cancellation", _(__name__ + '.DocumentEventType.' + 'CANCELLATION')

class DocumentACLAccessType(EnumUtilsMixin, models.TextChoices):
    CREATE = "Create", _(__name__ + '.DocumentACLAcessType.' + 'CREATE')
    MODIFY = "Modify", _(__name__ + '.DocumentACLAcessType.' + 'MODIFY')
    SAVE = "Save", _(__name__ + '.DocumentACLAcessType.' + 'SAVE')
    CANCEL = "Cancel", _(__name__ + '.DocumentACLAcessType.' + 'CANCEL')
    VIEW = "View", _(__name__ + '.DocumentACLAcessType.' + 'VIEW')
    PRINT = "Print", _(__name__ + '.DocumentACLAcessType.' + 'PRINT')
    ALL = "All",  _(__name__ + '.DocumentACLAcessType.' + 'ALL')
    NONE = "None", _(__name__ + '.DocumentACLAcessType.' + 'NONE')

  

class FormDefinitionACLAccessType(EnumUtilsMixin, models.TextChoices):
    CREATE = "Create", _(__name__ + '.FormDefinitionACLAccessType.' + 'CREATE')
    SEARCH = "Search", _(__name__ + '.FormDefinitionACLAccessType.' + 'SEARCH')
    ALL = "All", _(__name__ + '.FormDefinitionACLAccessType.' + 'ALL')
    NONE = "None", _(__name__ + '.FormDefinitionACLAccessType.' + 'NONE')


class DocumentOriginType(EnumUtilsMixin, models.TextChoices):
    ONLINE = "Online", _(__name__ + '.DocumentOriginType.' + 'ONLINE')
    UNKNOWN = "Unknown", _(__name__ + '.DocumentOriginType.' + 'UNKNOWN')

class DocumentStatusType(EnumUtilsMixin, models.TextChoices):
    DRAFTED = "Drafted", _(__name__ + '.DocumentStatusType.' + 'DRAFTED')
    DELETED = "Deleted", _(__name__ + '.DocumentStatusType.' + 'DELETED')
    SAVED = "Saved", _(__name__ + '.DocumentStatusType.' + 'SAVED')
    CANCELLED = "Cancelled", _(__name__ + '.DocumentStatusType.' + 'CANCELLED')


class ExternalFunctionExecutionModeType(EnumUtilsMixin, models.TextChoices):
    DRAFT_LOAD = "DRAFT_LOAD", _(__name__ + '.ExternalFunctionExecutionModeType.' +
                       'DRAFT_LOAD')
    CREATION_TIME = "CREATION_TIME", _(__name__ + '.ExternalFunctionExecutionModeType.' +
                          'CREATION_TIME')
    RUNTIME = "RUNTIME", _(__name__ + '.ExternalFunctionExecutionModeType.' +
                    'RUNTIME')
    INACTIVE = "INACTIVE", _(__name__ + '.ExternalFunctionExecutionModeType.' +
                     'INACTIVE')
    SAVE_TIME = "SAVE_TIME", _(__name__ + '.ExternalFunctionExecutionModeType.' +
                      'SAVE_TIME')

class FormClassStatusType(EnumUtilsMixin, models.TextChoices):
    DEVELOPMENT = "Development",  _(__name__ + '.FormClassStatusType.' + 'DEVELOPMENT')
    PRODUCTION = "Production", _(__name__ + '.FormClassStatusType.' + 'PRODUCTION')
    DEACTIVATED = "Deactivated",  _(__name__ + '.FormClassStatusType.' + 'DEACTIVATED')


class FormDefinitionStatusType(EnumUtilsMixin, models.TextChoices):
    DEVELOPMENT = "Development",  _(__name__ + '.FormDefinitionStatusType.' +
                        'DEVELOPMENT')
    PRODUCTION = "Production", _(__name__ + '.FormDefinitionStatusType.' + 'PRODUCTION')
    DEACTIVATED = "Deactivated",  _(__name__ + '.FormDefinitionStatusType.' +
                        'DEACTIVATED')

class FormClassType(EnumUtilsMixin, models.TextChoices):
    ADMINISTRATIVE = "Administrative", _(__name__ + '.FormClassType.' + 'ADMINISTRATIVE')
    OBLIGATION_BASED = "Obligation Based", _(__name__ + '.FormClassType.' + 'OBLIGATION_BASED')

   