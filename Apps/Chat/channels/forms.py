from django import forms



class MessagesForm(forms.Form):
    message = forms.CharField(max_length=1000, min_length=1, required=True)
