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
        add_attr_placeholder(
            self.fields['first_name'], 'Type your first name here. Ex.: João')
        add_attr_placeholder(
            self.fields['last_name'], 'Type your last name here. Ex.: Campos')

    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=4, max_length=150,
        help_text='Your password must be between 4 and 150 characters long'

    )
    first_name = forms.CharField(

        label='First Name',
        error_messages={'required': 'Write your first name'},

    )
    last_name = forms.CharField(
        label='Last Name',
        error_messages={'required': 'Write your last name'}
    )

    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            'placeholder': 'Type your email here'
        }),
        error_messages={'required': 'This field must not be empty'},
        help_text=('This email must be valid'),
        label='Email address',
    )
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
        'required': 'Password must not be empty'
    },

        help_text=('Password must have at least one uppercase letter, '
                   'one lowercase letter and one number. The length should be '
                   'at least 8 characters.'),
        validators=[strong_password],
        label='Password'

    )

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repeat your password'
        }
    ),
        error_messages={'required': 'Please, repeat your password'},
        label='Confirm'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Passwords do not match', code='invalid')
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,
            })
