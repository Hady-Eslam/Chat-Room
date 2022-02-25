from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=100, required=True)
    password = forms.CharField(min_length=1, max_length=100, required=True)


class ForgetPasswordForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=100, required=True)


class ResetPasswordForm(forms.Form):
    password = forms.CharField(min_length=1, max_length=100, required=True)
