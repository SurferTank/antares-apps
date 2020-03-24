from antares.apps.client.models import Client, ClientType
from datetime import datetime

from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext as _

from ..constants import UserClassType
from ..models import Role, UserRole, User


# from django.contrib.auth.forms import UserCreationForm
class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    user_class = forms.TypedChoiceField(choices=UserClassType.choices())
    captcha = ReCaptchaField()
    field_order = [
        'first_name', 'last_name', 'email', 'username', 'password',
        'user_class', 'captcha'
    ]

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        if (self.cleaned_data.get('user_class') is not None):
            role = Role.find_one_by_code(
                self.cleaned_data.get('user_class').upper() + "_ROLE")
            user_role = UserRole()
            user_role.author = user
            user_role.user = user
            user_role.role = role
            user_role.start_date = datetime.now()
            user_role.save()
        # the role to which all users pertain
        basic_role = Role.find_one_by_code("BASIC_ROLE")
        user_role = UserRole()
        user_role.author = user
        user_role.user = user
        user_role.role = basic_role
        user_role.start_date = datetime.now()
        user_role.save()

        # simple client so the accounts and documents work.
        client = Client()
        client.user = user
        client.first_name = user.first_name
        client.last_name = user.last_name
        client.registration_date = timezone.now()
        client_type = ClientType.find_one("Individual")
        client.client_type = client_type
        client.save()

    # def save(self):
    #    from antares.apps.user.models import Role
    #    role = Role.find_one_by_code(self.user_role)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
