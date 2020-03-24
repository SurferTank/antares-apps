'''
Created on Jun 23, 2016

@author: leobelen
'''
from antares.apps.core.mixins import EnumUtilsMixin

from django.db import models
from django.utils.translation import ugettext as _


class ItemStatusType(EnumUtilsMixin, models.TextChoices):
    ACTIVE = "Active", _(__name__ + '.StatusType.' + "ACTIVE")
    INACTIVE = "Inactive", _(__name__ + '.StatusType.' + "INACTIVE")


class AddressType(EnumUtilsMixin, models.TextChoices):
    REAL = "Real", _(__name__ + '.AddressType.' + "REAL")
    LEGAL = "Legal", _(__name__ + '.AddressType.' + "LEGAL")
    ESPECIAL = "Especial", _(__name__ + '.AddressType.' + "ESPECIAL")


class ClientArchetype(EnumUtilsMixin, models.TextChoices):
    INDIVIDUAL = "Individual", _(__name__ + '.ClientArchetype.' + "INDIVIDUAL")
    CORPORATE = "Corporate", _(__name__ + '.ClientArchetype.' + "CORPORATE")


class ClientStatusType(EnumUtilsMixin, models.TextChoices):
    ACTIVE = "Active", _(__name__ + '.ClientStatusType.' + 'ACTIVE')
    DEFUNCT = "Defunct", _(__name__ + '.ClientStatusType.' + 'DEFUCT')
    DEFUNCT_CANDIDATE = "Defunct Candidate", _(__name__ + '.ClientStatusType.' + 'DEFUNCT_CANDIDATE')


class TelephoneItemType(EnumUtilsMixin, models.TextChoices):
    HOME = "Home", _(__name__ + '.TelephoneItemType.' + 'HOME')
    WORK = "Work", _(__name__ + '.TelephoneItemType.' + 'WORK')
    CELLPHONE = "Cellphone", _(__name__ + '.TelephoneItemType.' + 'CELLPHONE')
    OTHER = "Other", _(__name__ + '.TelephoneItemType.' + 'OTHER')


class SocialNetworkItemType(EnumUtilsMixin, models.TextChoices):
    SKYPE = "Skype", _(__name__ + '.SocialNetworkItemType.' + "SKYPE")


class ClientRelationType(EnumUtilsMixin, models.TextChoices):
    OWNER = "Owner", _(__name__ + '.ClientRelationType.' + 'OWNER')
    DIRECTOR = "Director", _(__name__ + '.ClientRelationType.' + 'DIRECTOR')
    ACCOUNTANT = "Accountant", _(__name__ + '.ClientRelationType.' + 'ACCOUNTANT')
    LAWYER = "Lawyer", _(__name__ + '.ClientRelationType.' + 'LAWYER')
    CLERK = "Clerk", _(__name__ + '.ClientRelationType.' + 'CLERK')
    GENERIC_WORKER = 'Worker', _(__name__ + '.ClientRelationType.' + 'GENERIC_WORKER')  # this one has no executive relation

                           
class ClientRelationPermissionType(EnumUtilsMixin, models.TextChoices):
    ALL = "All", _(__name__ + '.ClientRelationPermissionType.' + "ALL")
    FILE = "File", _(__name__ + '.ClientRelationPermissionType.' + "FILE")


class ClientGenderType(EnumUtilsMixin, models.TextChoices):
    MALE = "Male", _(__name__ + '.ClientGenderType.' + "MALE")
    FEMALE = "Female", _(__name__ + '.ClientGenderType.' + "FEMALE")


class EmailType(EnumUtilsMixin, models.TextChoices):
    OFFICIAL = "Official", _(__name__ + '.EmailType.' + 'OFFICIAL')
    HOME = "Home", _(__name__ + '.EmailType.' + 'HOME')
    WORK = "Work", _(__name__ + '.EmailType.' + 'WORK')
    OTHER = "Other", _(__name__ + '.EmailType.' + 'OTHER')
