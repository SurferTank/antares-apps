# __init__.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .application import Application
from .application_parameter import ApplicationParameter
from .org_unit import OrgUnit
from .role import Role
from .role_application import RoleApplication
from .user import User
from .user_org_unit import UserOrgUnit
from .user_role import UserRole


__all__ = [
    'User',
    'OrgUnit',
    'UserOrgUnit',
    'Role',
    'UserRole',
    'Application',
    'RoleApplication',
    'ApplicationParameter',
]


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)