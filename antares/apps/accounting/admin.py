from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import AccountRule
from .models import AccountType
from .models import GLAccountType
from .models import TransactionType


admin.site.register(GLAccountType, MPTTModelAdmin)
admin.site.register(AccountRule)
admin.site.register(AccountType)
admin.site.register(TransactionType)
