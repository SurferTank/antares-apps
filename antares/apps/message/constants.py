from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class MessageType(EnumUtilsMixin, Enum):
    FORM_DEFINITION = "Form Definition"
    FLOW_DEFINITION = "Flow Definition"
    CURRENT_ACCOUNT = "Current Account"
    FLOW_CASE = "Flow Case"
    DOCUMENT = "Document"
    EXTERNAL_SYSTEM = "External System"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        FORM_DEFINITION = _(__name__ + '.MessageType.' + 'FORM_DEFINITION')
        FLOW_DEFINITION = _(__name__ + '.MessageType.' + 'FLOW_DEFINITION')
        CURRENT_ACCOUNT = _(__name__ + '.MessageType.' + 'CURRENT_ACCOUNT')
        FLOW_CASE = _(__name__ + '.MessageType.' + 'FLOW_CASE')
        DOCUMENT = _(__name__ + '.MessageType.' + 'DOCUMENT')
        EXTERNAL_SYSTEM = _(__name__ + '.MessageType.' + 'EXTERNAL_SYSTEM')


class MessageStatusType(EnumUtilsMixin, Enum):
    PENDING = "Pending"
    PROCESSED = "Processed"
    WITH_ERRORS = "With Errors"
    ON_HOLD = "On hold"
    CANCELLED = "Cancelled"
    EXTERNAL_SYSTEM = "External System"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        PENDING = _(__name__ + '.MessageStatusType.' + 'PENDING')
        PROCESSED = _(__name__ + '.MessageStatusType.' + 'PROCESSED')
        WITH_ERRORS = _(__name__ + '.MessageStatusType.' + 'WITH_ERRORS')
        ON_HOLD = _(__name__ + '.MessageStatusType.' + 'ON_HOLD')
        CANCELLED = _(__name__ + '.MessageStatusType.' + 'CANCELLED')
