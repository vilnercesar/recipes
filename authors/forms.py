import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_attr_placeholder(field, attr_new_val):
    add_attr(field, 'placeholder', attr_new_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError('Type a strong password', code='invalid')


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr_placeholder(
            self.fields['username'], 'Type your username here')
        add_attr_placeholder(self.fields['email'], 'Type your email here')

    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
        'required': 'Password must not be empty'
    },

        help_text=('Password must have at least one uppercase letter, '
                   'one lowercase letter and one number. The length should be '
                   'at least 8 characters.'),
        validators=[strong_password]
    )

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repeat your password'
        }
    ))

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'Email address',
            'password': 'Password'

        }

        help_texts = {
            'email': 'This email must be valid',
        }
        erros_messages = {
            'user_name': {
                'required': 'This field not be empty'
            }

        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here Ex.: João'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Type your last'
                                                'name here Ex.: Campos'})

        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'teste' in data:
            raise ValidationError('Não digite %(value)s no campo password',
                                  code='invalid',
                                  params={'value': '"teste"'}

                                  )
        return data

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': 'Passwords do not match',
            })
