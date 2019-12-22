from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Application
from .models import ApplicationParameter
from .models import OrgUnit
from .models import Role
from .models import RoleApplication
from .models import UserOrgUnit
from .models import UserRole


admin.site.register(UserOrgUnit)
admin.site.register(OrgUnit, MPTTModelAdmin)
admin.site.register(UserRole)
admin.site.register(Role, MPTTModelAdmin)
admin.site.register(RoleApplication)
admin.site.register(Application, MPTTModelAdmin)
admin.site.register(ApplicationParameter)
