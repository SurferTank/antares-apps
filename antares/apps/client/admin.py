from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import AddressItem
from .models import AttributeDefinition
from .models import Client
from .models import ClientAttribute
from .models import ClientBranch
from .models import ClientBusinessClassification
from .models import ClientIdentificationType
from .models import ClientType
from .models import ClientUserRelation
from .models import ClientUserRelationPermission
from .models import EmailItem
from .models import IdentificationItem
from .models import IsicPosition
from .models import SocialNetworkItem
from .models import TelephoneItem


admin.site.register(ClientIdentificationType)
admin.site.register(AttributeDefinition)
admin.site.register(ClientType)
admin.site.register(Client)


@admin.register(ClientUserRelation)
class ClientUserRelationAdmin(admin.ModelAdmin):
    list_display = ('parent_user', 'child_client' , 'relation_type', 'start_date', 'end_date')


@admin.register(ClientUserRelationPermission)
class ClientUserRelationPermissionAdmin(admin.ModelAdmin):
    list_display = ('client_relation', 'relation_type', 'start_date', 'end_date')

    
admin.site.register(ClientBranch)
admin.site.register(TelephoneItem)
admin.site.register(AddressItem)
admin.site.register(EmailItem)
admin.site.register(SocialNetworkItem)
admin.site.register(ClientBusinessClassification)
admin.site.register(IdentificationItem)
admin.site.register(ClientAttribute)
admin.site.register(IsicPosition, MPTTModelAdmin)
