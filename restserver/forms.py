from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import User, UserManager


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label = _('Email'),
        required = True,
        widget = forms.EmailField(
            attrs = {
                'class': 'form-control',
                'placeholder': _('Email address'),
                'required': 'True',
            }
        )
    )
    username = forms.CharField(
        label = _('Username'),
        required = True,
        widget = forms.TextInput(
            attrs = {
                'class': 'form-control',
                 'placeholder': _('Username'),
                'required': 'True',
            }
        ) 
    )
    password1 = forms.CharField(
        label = _('Password'),
        widget = forms.PasswordInput(
            attrs = {
                'class': 'form-control',
                'placeholder': _('Password'),
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label = _('Password confirmation'),
        widget = forms.PasswordInput(
            attrs = {
                'calss': 'form-control',
                'placeholder': _('Password confirmation'),
                'required': 'True', 
            }
        )
    )


def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
        raise forms.ValidationError("Passwords don't match")
    return password2

def save(self, commit=True):
    user = super(UserCreationForm,self).save(commit=False)
    user.email = UserManager.normalize_email(self.cleaned_data['email'])
    if commit:
        user.save()
    return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label =_ ('Password')
    )

    def clean_password(self):
        return self.initial["password"]