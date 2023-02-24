from django import forms

from utils.django_forms import add_attr_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr_placeholder(self.fields['username'], 'Type your username')

    username = forms.CharField()

    password = forms.CharField(widget=forms.PasswordInput())
