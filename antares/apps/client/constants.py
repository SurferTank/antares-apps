'''
Created on Jun 23, 2016

@author: leobelen
'''
from enumfields import Enum

from django.utils.translation import ugettext as _
from antares.apps.core.mixins import EnumUtilsMixin


class ItemStatusType(EnumUtilsMixin, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ACTIVE = _(__name__ + '.StatusType.' + "ACTIVE")
        INACTIVE = _(__name__ + '.StatusType.' + "INACTIVE")


class AddressType(EnumUtilsMixin, Enum):
    REAL = "Real"
    LEGAL = "Legal"
    ESPECIAL = "Especial"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        REAL = _(__name__ + '.AddressType.' + "REAL")
        LEGAL = _(__name__ + '.AddressType.' + "LEGAL")
        ESPECIAL = _(__name__ + '.AddressType.' + "ESPECIAL")


class ClientArchetype(EnumUtilsMixin, Enum):
    INDIVIDUAL = "Individual"
    CORPORATE = "Corporate"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        INDIVIDUAL = _(__name__ + '.ClientArchetype.' + "INDIVIDUAL")
        CORPORATE = _(__name__ + '.ClientArchetype.' + "CORPORATE")


class ClientStatusType(EnumUtilsMixin, Enum):
    ACTIVE = "Active"
    DEFUNCT = "Defunct"
    DEFUNCT_CANDIDATE = "Defunct Candidate"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ACTIVE = _(__name__ + '.ClientStatusType.' + 'ACTIVE')
        DEFUNCT = _(__name__ + '.ClientStatusType.' + 'DEFUNCT')
        DEFUNCT_CANDIDATE = _(__name__ + '.ClientStatusType.' +
                              'DEFUNCT_CANDIDATE')


class TelephoneItemType(EnumUtilsMixin, Enum):
    HOME = "Home"
    WORK = "Work"
    CELLPHONE = "Cellphone"
    OTHER = "Other"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        HOME = _(__name__ + '.TelephoneItemType.' + 'HOME')
        WORK = _(__name__ + '.TelephoneItemType.' + 'WORK')
        CELLPHONE = _(__name__ + '.TelephoneItemType.' + 'CELLPHONE')
        OTHER = _(__name__ + '.TelephoneItemType.' + 'CELLPHONE')


class SocialNetworkItemType(EnumUtilsMixin, Enum):
    SKYPE = "Skype"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        SKYPE = _(__name__ + '.SocialNetworkItemType.' + "SKYPE")


class ClientRelationType(EnumUtilsMixin, Enum):
    OWNER = "Owner"
    DIRECTOR = "Director"
    ACCOUNTANT = "Accountant"
    LAWYER = "Lawyer"
    CLERK = "Clerk"
    GENERIC_WORKER = 'Worker'  # this one has no executive relation

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        OWNER = _(__name__ + '.ClientRelationType.' + 'OWNER')
        DIRECTOR = _(__name__ + '.ClientRelationType.' + 'DIRECTOR')
        ACCOUNTANT = _(__name__ + '.ClientRelationType.' + 'ACCOUNTANT')
        LAWYER = _(__name__ + '.ClientRelationType.' + 'LAWYER')
        CLERK = _(__name__ + '.ClientRelationType.' + 'CLERK')
        GENERIC_WORKER = _(__name__ + '.ClientRelationType.' +
                           'GENERIC_WORKER')


class ClientRelationPermissionType(EnumUtilsMixin, Enum):
    ALL = "All"
    FILE = "File"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        ALL = _(__name__ + '.ClientRelationPermissionType.' + "ALL")
        FILE = _(__name__ + '.ClientRelationPermissionType.' + "FILE")


class ClientGenderType(EnumUtilsMixin, Enum):
    MALE = "Male"
    FEMALE = "Female"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        MALE = _(__name__ + '.ClientGenderType.' + "MALE")
        FEMALE = _(__name__ + '.ClientGenderType.' + "FEMALE")


class EmailType(EnumUtilsMixin, Enum):
    OFFICIAL = "Official"
    HOME = "Home"
    WORK = "Work"
    OTHER = "Other"

    def __str__(self):
        """
        Just returns the value of the Enumeration
        """
        return str(self.value)

    class Labels:
        OFFICIAL = _(__name__ + '.EmailType.' + 'OFFICIAL')
        HOME = _(__name__ + '.EmailType.' + 'HOME')
        WORK = _(__name__ + '.EmailType.' + 'WORK')
        OTHER = _(__name__ + '.EmailType.' + 'OTHER')
