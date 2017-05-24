from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import ActionDefinition
from .models import Catalog
from .models import ConceptType
from .models import Currency
from .models import Holiday
from .models import HrnCode
from .models import SystemParameter
from .models import UserParameter

admin.site.register(ConceptType, MPTTModelAdmin)
admin.site.register(Currency)
admin.site.register(Holiday)
admin.site.register(Catalog)
admin.site.register(HrnCode)
admin.site.register(SystemParameter)
admin.site.register(UserParameter)
admin.site.register(ActionDefinition)
