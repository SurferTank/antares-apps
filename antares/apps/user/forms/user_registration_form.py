from datetime import datetime
from django.utils.translation import ugettext as _
from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from ..constants import UserClassType
from ..models import Role, UserRole, User

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    user_class = forms.TypedChoiceField(choices=UserClassType.choices())

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        role = Role.find_one_by_code(self.cleaned_data.get('user_class').upper() + "_ROLE")
        user_role = UserRole()
        user_role.author = user
        user_role.user = user
        user_role.role = role
        user_role.start_date = datetime.now()
        user_role.save()
        
    
    #def save(self):
    #    from antares.apps.user.models import Role
    #    role = Role.find_one_by_code(self.user_role)
        
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )