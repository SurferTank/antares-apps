from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Application
from .models import ApplicationParameter
from .models import OrgUnit
from .models import Role
from .models import RoleApplication
from .models import UserOrgUnit
from .models import UserRole

@admin.register(UserOrgUnit)
class UserOrgUnitAdmin(admin.ModelAdmin):
    list_display = ('user', 'org_unit',
                    'start_date', 'end_date'
                    )

admin.site.register(OrgUnit, MPTTModelAdmin)
@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role',
                    'start_date', 'end_date'
                    )
admin.site.register(Role, MPTTModelAdmin)

@admin.register(RoleApplication)
class RoleApplicationAdmin(admin.ModelAdmin):
    list_display = ('role', 'application',
                    'start_date', 'end_date'
                    )

admin.site.register(Application, MPTTModelAdmin)
admin.site.register(ApplicationParameter)
