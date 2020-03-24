from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Application
from .models import ApplicationParameter
from .models import OrgUnit
from .models import Role
from .models import RoleApplication
from .models import User
from .models import UserOrgUnit
from .models import UserRole


admin.site.register(User)


@admin.register(UserOrgUnit)
class UserOrgUnitAdmin(admin.ModelAdmin):
    list_display = ('user', 'org_unit',
                    'start_date', 'end_date'
                    )


@admin.register(OrgUnit)
class OrgUnitAdmin(admin.ModelAdmin):
    list_display = ('code', 'name',
                    'parent'
                    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role',
                    'start_date', 'end_date'
                    )


@admin.register(Role)
class RolenAdmin(MPTTModelAdmin):
    list_display = ('code', 'name',
                    'parent'
                    )

    
@admin.register(RoleApplication)
class RoleApplicationAdmin(admin.ModelAdmin):
    list_display = ('role', 'application',
                    'start_date', 'end_date'
                    )


@admin.register(Application)
class ApplicationAdmin(MPTTModelAdmin):
    list_display = ('application_name', 'parent',
                    'url', 'route', 'scope'
                    )


admin.site.register(ApplicationParameter)
