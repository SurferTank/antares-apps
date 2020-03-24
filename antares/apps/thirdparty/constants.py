from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class ThirdPartyRecordStatusType(EnumUtilsMixin, models.TextChoices):
    OPEN = "Open", _(__name__ + '.ThirdPartyRecordStatusType.' + 'OPEN')
    PROCESSING = "Processing", _(__name__ + '.ThirdPartyRecordStatusType.' + 
                       'PROCESSING')
    PROCESSED = "Processed", _(__name__ + '.ThirdPartyRecordStatusType.' + 'PROCESSED')
    CLOSED = "Closed", _(__name__ + '.ThirdPartyRecordStatusType.' + 'CLOSED')
    ERROR = "Error", _(__name__ + '.ThirdPartyRecordStatusType.' + 'ERROR')
    ON_HOLD = "On hold", _(__name__ + '.ThirdPartyRecordStatusType.' + 'ON_HOLD')


class ThirdPartyDetailStatusType(EnumUtilsMixin, models.TextChoices):
    OPEN = "Open", _(__name__ + '.ThirdPartyDetailStatusType.' + 'OPEN')
    PROCESSING = "Processing", _(__name__ + '.ThirdPartyDetailStatusType.' + 
                       'PROCESSING')
    PROCESSED = "Processed", _(__name__ + '.ThirdPartyDetailStatusType.' + 'PROCESSED')
    CLOSED = "Closed", _(__name__ + '.ThirdPartyDetailStatusType.' + 'CLOSED')
    ERROR = "Error", _(__name__ + '.ThirdPartyDetailStatusType.' + 'ERROR')
    ON_HOLD = "On hold", _(__name__ + '.ThirdPartyDetailStatusType.' + 'ON_HOLD')


class ThirdPartyChannelType(EnumUtilsMixin, models.TextChoices):
    WEB = "Web", _(__name__ + '.ThirdPartyChannelType.' + 'WEB')
    SOA = "Soa", _(__name__ + '.ThirdPartyChannelType.' + 'SOA')

