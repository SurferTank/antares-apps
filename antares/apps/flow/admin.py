from django.contrib import admin
from antares.apps.flow.models.definition import FlowPackage, FlowDefinition
from .manager import FlowAdminManager

# Register your models here.
@admin.register(FlowPackage)
class FlowPackageAdmin(admin.ModelAdmin):
    list_display = ('package_id',  
                    'package_name', 
                    'package_version')
    def save_model(self, request, obj, form, change):
        manager = FlowAdminManager(obj.xpdl)
        manager.load_xpdl()
        obj.save()
        
@admin.register(FlowDefinition)
class FlowDefinitionAdmin(admin.ModelAdmin):
    list_display = ('flow_id',  
                    'status', 
                    'valid_from', 
                    'valid_to')
    