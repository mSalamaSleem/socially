from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileSettingForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_pic', 'bio']
