from django.contrib import admin

from .models import DocumentACL
from .models import FormClass
from .models import FormDefinition
from .models import FormDefinitionACL


class FormDefinitionAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.process_form_definition_loading()
        obj.save()


admin.site.register(FormClass)
admin.site.register(FormDefinition, FormDefinitionAdmin)
admin.site.register(DocumentACL)
admin.site.register(FormDefinitionACL)

# Register your models here.
