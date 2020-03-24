from django.contrib import admin

from .models import ObligationRule


@admin.register(ObligationRule)
class ObligationRuleAdmin(admin.ModelAdmin):
    list_display = ('form_definition', 'concept_type',
                    'account_type', 'active',
                    'base_date', 'last_run', 'next_run',
                    'obligation_type', 'periodicity_type',
                    'time_unit_type',
                    )
