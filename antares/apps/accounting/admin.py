from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import AccountRule
from .models import AccountType
from .models import GLAccountType
from .models import TransactionType
from .models import InterestDefinition
from .models import PenaltyDefinition


admin.site.register(GLAccountType, MPTTModelAdmin)
admin.site.register(AccountRule)
admin.site.register(InterestDefinition)
admin.site.register(PenaltyDefinition)
@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_type_name' , 'auxiliary_account', 
                    'include_interest', 'include_penalties', 'is_document_based',
                    'active', 
                    )
@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction_type_name', 'effect', 
                    'inverse_transaction_type', 'calculate_charges', 
                    'post_zeros', 'active',
                    )

