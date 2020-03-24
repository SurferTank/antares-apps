from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class MessageType(EnumUtilsMixin, models.TextChoices):
    FORM_DEFINITION = "Form Definition", _(__name__ + '.MessageType.' + 'FORM_DEFINITION')
    FLOW_DEFINITION = "Flow Definition", _(__name__ + '.MessageType.' + 'FLOW_DEFINITION')
    CURRENT_ACCOUNT = "Current Account", _(__name__ + '.MessageType.' + 'CURRENT_ACCOUNT')
    FLOW_CASE = "Flow Case", _(__name__ + '.MessageType.' + 'FLOW_CASE')
    DOCUMENT = "Document", _(__name__ + '.MessageType.' + 'DOCUMENT')
    EXTERNAL_SYSTEM = "External System", _(__name__ + '.MessageType.' + 'EXTERNAL_SYSTEM')


class MessageStatusType(EnumUtilsMixin, models.TextChoices):
    PENDING = "Pending", _(__name__ + '.MessageStatusType.' + 'PENDING')
    PROCESSED = "Processed", _(__name__ + '.MessageStatusType.' + 'PROCESSED')
    WITH_ERRORS = "With Errors", _(__name__ + '.MessageStatusType.' + 'WITH_ERRORS')
    ON_HOLD = "On hold", _(__name__ + '.MessageStatusType.' + 'ON_HOLD')
    CANCELLED = "Cancelled", _(__name__ + '.MessageStatusType.' + 'CANCELLED')
    EXTERNAL_SYSTEM = "External System", _(__name__ + '.MessageStatusType.' + 'EXTERNAL_SYSTEM')
