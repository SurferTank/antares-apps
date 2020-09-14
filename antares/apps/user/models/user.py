# -*- coding: utf-8 -*-
from antares.apps.client.constants import ClientRelationType
from antares.apps.core.middleware.request import get_request
import logging
from uuid import UUID
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ..exceptions import UserException
from .role_application import RoleApplication
from .user_org_unit import UserOrgUnit
from .user_role import UserRole


logger = logging.getLogger(__name__)


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_(__name__ + ".id"),
        help_text=_(__name__ + ".primary_key_help"))

    def __str__(self):
        return self.username

    def get_current_org_unit_list(self):
        """
        Gets the list of units for which the user is enroled now
        """
        unit_list = []

        for user_org_unit in self.user_org_unit_set.select_related().filter(
                Q(start_date__gte=timezone.now()) & 
            (Q(end_date__lte=timezone.now()) | Q(end_date=None))):
            unit_list.append(user_org_unit.org_unit)
        return unit_list

    def get_current_role_list(self):
        """
        Gets the list of roles for which the user is enroled now
        """
        role_list = []

        for user_role in self.user_role_set.select_related().filter(
                Q(start_date__gte=timezone.now()) & 
            (Q(end_date__lte=timezone.now()) | Q(end_date=None))):
            role_list.append(user_role.role)
        return role_list

    def set_on_behalf_client(self, client):
        try:
            if (self.client is not None and client.id != self.client.id):
                try:
                    get_request().user.client_user_relation_set \
                        .select_related().filter(Q(child_client=client) & \
                            Q(start_date__lte=timezone.now()) & (
                            Q(end_date__gte=timezone.now()) | 
                            Q(end_date=None))) \
                        .exclude(relation_type=str(ClientRelationType.GENERIC_WORKER))\
                        .order_by('update_date')[:1].get()
                    get_request().session['on_behalf_client'] = str(client.id)
                    return client
                except:
                    raise PermissionDenied(_(__name__ + \
                                              ".user_has_no_relation_with_client {client_id}").format(
                                                  client_id=client.id))
            elif client.id == self.client.id:
                get_request().session['on_behalf_client'] = None
                return None
        except:
            raise UserException(
                _(__name__ + ".the_user_has_no_client_associated"))

    def get_on_behalf_client(self):
        from antares.apps.client.models import Client
        try:
            if ('on_behalf_client' in get_request().session
                    and get_request().session['on_behalf_client'] is not None):
                return Client.find_one(
                    UUID(get_request().session['on_behalf_client']))
        except Exception as e:
            raise UserException(
                _(__name__ + ".the_user_has_no_client_associated"))
        # try:
        #    settings.TEST_MODE
        # except:
        #    settings.TEST_MODE = False

        # if settings.TEST_MODE == False:
        try:
            if (self.client is not None):
                return self.client
        except:
            return None
        # else:
        #    return None

    @classmethod
    def find_one(cls, user_id):
        if isinstance(user_id, str):
            user_uuid = uuid.UUID(user_id)
        elif isinstance(user_id, uuid.UUID):
            user_uuid = user_id
        elif isinstance(user_id, User):
            return user_id
        try:
            return User.objects.get(id=user_uuid)
        except User.DoesNotExist:
            return None

    @classmethod
    def find_one_by_user_name(cls, username):

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @classmethod
    def find_one_by_username(cls, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_system_user(cls):
        from antares.apps.core.models import SystemParameter
        from antares.apps.core.constants import FieldDataType
        """
        Returns the system user, an special (deactivated) user, which serves as wildcard for actions taken by the system without
        human intervention.
        """
        system_username = SystemParameter.find_one(
            "SYSTEM_USERNAME", FieldDataType.STRING, "system")
        system_user = User.find_one_by_username(system_username)
        if (system_user is not None):
            return system_user
        system_email = SystemParameter.find_one(
            "SYSTEM_EMAIL", FieldDataType.STRING, "system@surfertank.com")

        system_user = User.objects.create(
            username=system_username,
            email=system_email,
            is_staff=True,
            is_active=False)
        # we don't want anyone to take over, so an UUID would be random enough
        system_user.set_password(str(uuid.uuid4()))
        system_user.save()
        return system_user

    @classmethod
    def get_test_user(cls):
        """
        Returns a test user for executing tests. If we are not running 
        """
        try:
            settings.TEST_MODE
        except:
            settings.TEST_MODE = False
        if (settings.TEST_MODE == True):
            test_user = cls.find_one_by_user_name("testuser")
            if (test_user is None):
                test_user = User.objects.create(
                    username="testuser",
                    email="testuser@surfertank.com",
                    is_staff=True,
                    is_active=False)
                # we don't want anyone to take over, so an UUID would be random enough
                test_user.set_password("12345")
                test_user.save()
        else:
            test_user = None
        return test_user

    def get_role_list(self, include_children=True):
        """
        Gets the role list along with all its decendants by default.
        """
        roles = set()
        for user_role in self.role_set.select_related().filter(
                Q(start_date__lte=timezone.now()) & 
            (Q(end_date__gte=timezone.now()) | Q(end_date=None))):
            roles.add(user_role.role)
            if include_children == True:
                self._get_role_children_list(roles, user_role.role)

        return list(roles)

    def _get_role_children_list(self, roles, user_role):
        if user_role.is_leaf_node():
            return roles
        else:
            for role in user_role.get_children():
                roles.add(role)
                self._get_role_children_list(roles, user_role)
            return roles

    def get_role_string_list(self, include_children=True):
        user_roles = list()
        roles = self.get_role_list(include_children)
        for role in roles:
            user_roles.append(role.code)
        return user_roles

    def check_roles(self,
                    roles,
                    include_children=True,
                    consider_super_user=True):
        ''' Checks if an user is included on a role '''
        user_roles = self.get_role_string_list()
        if isinstance(roles, str):
            roles = (roles,)

        for role in roles:
            if role in user_roles:
                return True
            else:
                # if consider_super_user == True and self.is_superuser==True:
                #    return True
                return False

    def get_org_unit_list(self):
        """
        
        """
        org_units = []
        for org_unit in self.org_unit_set.select_related().filter(
                Q(start_date__lte=timezone.now()) & 
            (Q(end_date__gte=timezone.now()) | Q(end_date=None))):
            org_units.append(org_unit.org_unit)
        return org_unit

    def has_role(self, role_code):
        """
        
        """
        for user_role in self.role_set.select_related().filter(
                Q(start_date__lte=timezone.now()) & 
            (Q(end_date__gte=timezone.now())
             | Q(end_date=None))).filter(role__code=role_code):
            return True
        return False

    def get_application_list(self):
        apps = set()
        for role in self.get_role_list():
            for role_app in role.application_set.select_related().filter(
                    Q(start_date__lte=timezone.now()) & 
                (Q(end_date__gte=timezone.now()) | Q(end_date=None))):
                if role_app.application not in apps:
                    apps.add(role_app.application)
        return apps

    @classmethod
    def find_active_users_in_role(cls, role):
        """
        
        """
        users = []
        roles = UserRole.objects.filter(role=role).filter(
            Q(start_date__lte=timezone.now()) & 
            (Q(end_date__gte=timezone.now()) | Q(end_date=None)))
        if (len(roles) > 0):
            for user in User.objects.filter(role_set__in=roles):
                users.append(user)

        return users

    @classmethod
    def find_active_users_in_org_unit(cls, org_unit):
        """
        
        """
        users = []
        org_units = UserOrgUnit.objects.filter(org_unit=org_unit).filter(
            Q(start_date__lte=timezone.now()) & 
            (Q(end_date__gte=timezone.now()) | Q(end_date=None)))
        if (len(org_units) > 0):
            for user in User.objects.filter(org_unit_set__in=org_units):
                users.append(user)

        return users

    @classmethod
    def find_by_user_id_org_unit_role(cls, user_id, org_unit, role):
        """
        
        """
        users = set()
        org_users = set()
        role_users = set()
        if (user_id is not None):
            if isinstance(user_id, str):
                user_id = uuid.UUID(user_id)
            user = User.find_one(user_id)
            if user is not None:
                org_users.add(user)
        if (org_unit is not None):
            org_users.update(cls.find_active_users_in_org_unit(org_unit))
        if (role is not None):
            role_users.update(cls.find_active_users_in_role(role))

        if (org_unit is not None and role_users is not None):
            users = org_users.intersection(role_users)
        elif org_unit is not None and role_users is None:
            users = org_users
        elif org_unit is None and role_users is not None:
            users = role_users

        return list(users)

    class Meta:
        app_label = 'user'
        db_table = 'user_user'
        verbose_name = _(__name__ + ".table_name")
        verbose_name_plural = _(__name__ + ".table_name_plural")
