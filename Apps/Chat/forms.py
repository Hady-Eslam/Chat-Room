from django import forms


class JoinRoomForm(forms.Form):
    password = forms.CharField(min_length=1, max_length=100, required=True)
