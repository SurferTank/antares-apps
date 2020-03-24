from django.contrib import admin

from .models import DocumentACL
from .models import FormClass
from .models import FormDefinition
from .models import FormDefinitionACL


@admin.register(FormDefinition)
class FormDefinitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'status',
                    'start_date', 'end_date')

    def save_model(self, request, obj, form, change):
        obj.process_form_definition_loading()
        obj.save()


@admin.register(FormClass)
class FormClasseAdmin(admin.ModelAdmin):
    list_display = ('id', 'type',
                    'status')
    

admin.site.register(DocumentACL)
admin.site.register(FormDefinitionACL)

# Register your models here.
