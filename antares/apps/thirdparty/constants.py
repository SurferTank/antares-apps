from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class ThirdPartyRecordStatusType(EnumUtilsMixin, Enum):
    OPEN = "Open"
    PROCESSING = "Processing"
    PROCESSED = "Processed"
    CLOSED = "Closed"
    ERROR = "Error"
    ON_HOLD = "On hold"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        OPEN = _(__name__ + '.ThirdPartyRecordStatusType.' + 'OPEN')
        PROCESSING = _(
            __name__ + '.ThirdPartyRecordStatusType.' + 'PROCESSING')
        PROCESSED = _(__name__ + '.ThirdPartyRecordStatusType.' + 'PROCESSED')
        CLOSED = _(__name__ + '.ThirdPartyRecordStatusType.' + 'CLOSED')
        ERROR = _(__name__ + '.ThirdPartyRecordStatusType.' + 'ERROR')
        ON_HOLD = _(__name__ + '.ThirdPartyRecordStatusType.' + 'ON_HOLD')


class ThirdPartyDetailStatusType(EnumUtilsMixin, Enum):
    OPEN = "Open"
    PROCESSING = "Processing"
    PROCESSED = "Processed"
    CLOSED = "Closed"
    ERROR = "Error"
    ON_HOLD = "On hold"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        OPEN = _(__name__ + '.ThirdPartyDetailStatusType.' + 'OPEN')
        PROCESSING = _(
            __name__ + '.ThirdPartyDetailStatusType.' + 'PROCESSING')
        PROCESSED = _(__name__ + '.ThirdPartyDetailStatusType.' + 'PROCESSED')
        CLOSED = _(__name__ + '.ThirdPartyDetailStatusType.' + 'CLOSED')
        ERROR = _(__name__ + '.ThirdPartyDetailStatusType.' + 'ERROR')
        ON_HOLD = _(__name__ + '.ThirdPartyDetailStatusType.' + 'ON_HOLD')


class ThirdPartyChannelType(EnumUtilsMixin, Enum):
    WEB = "Web"
    SOA = "Soa"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        WEB = _(__name__ + '.ThirdPartyChannelType.' + 'WEB')
        SOA = _(__name__ + '.ThirdPartyChannelType.' + 'SOA')
