from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import AccountRule
from .models import AccountType
from .models import GLAccountType
from .models import InterestDefinition
from .models import PenaltyDefinition
from .models import TransactionType


admin.site.register(GLAccountType, MPTTModelAdmin)


@admin.register(AccountRule)
class AccountRuleAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'form_definition', 'concept_type', 'amount_field')

    
@admin.register(InterestDefinition)
class InterestDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'periodicity', 'first_is_duedate',
                    'use_calendar_periods', 'concept_type', 'active')


@admin.register(PenaltyDefinition)
class PenaltyDefinitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'fixed_amount',
                    'periodicity', 'max_rounds',
                    'recurring', 'concept_type', 'active')


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

