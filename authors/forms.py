from django import forms
from django.contrib.auth.models import User


def add_attr_placeholder(field, attr_new_val):

    field.widget.attrs['placeholder'] = attr_new_val


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr_placeholder(
            self.fields['username'], 'Type your username here')
        add_attr_placeholder(self.fields['email'], 'Type your email here')
        add_attr_placeholder(self.fields['first_name'], 'Ex.: João')
        add_attr_placeholder(self.fields['last_name'], 'Ex.: Doe')

    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
        'required': 'Password must not be empty'
    },

        help_text=('Password must have at least one uppercase letter, '
                   'one lowercase letter and one number. The length should be '
                   'at least 8 characters.')
    )

    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Repeat your password'
        })

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
                'placeholder': 'Type your first name here'}),

            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }
