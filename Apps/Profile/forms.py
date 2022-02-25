from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(min_length=1, max_length=100, required=False)
    last_name = forms.CharField(min_length=1, max_length=100, required=False)
    class Meta:
        model = Profile
        exclude = ['user']


class PasswordForm(forms.Form):
    old_password = forms.CharField(min_length=1, max_length=100, required=True)
    password = forms.CharField(min_length=1, max_length=100, required=True)


class SettingsForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=100, required=True)
    password = forms.CharField(min_length=1, max_length=100, required=True)
