from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Guild,Student,Group
from django.forms import ModelForm

#Базовая форма регистрации для новой школы
class RegistrationForm(UserCreationForm):
  guild_name = forms.CharField(label=_('Название школы'),widget=forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Солнышко'
      }))

  password1 = forms.CharField(
      label=_("Пароль"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
  )
  password2 = forms.CharField(
      label=_("Повторите пароль"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
  )

  class Meta:
    model = User
    fields = ('username', 'email', )

    labels = {
      'username': _('Username'),
      'email': _('Email'),
    }
    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Username'
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'example@mail.com'
      })
    }


class SimpleRegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Пароль"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
  )
  password2 = forms.CharField(
      label=_("Повторите пароль"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
  )

  class Meta:
    model = User
    fields = ('username', 'email', )

    labels = {
      'username': _('Username'),
      'email': _('Email'),
    }
    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Username'
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'example@mail.com'
      })
    }

class UserLoginForm(AuthenticationForm):
  username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  password = forms.CharField(
      label=_("Пароль"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Пароль"}),
  )

class StudentCreationForm(ModelForm):
  class Meta:
    model = Student
    fields=["name",'gender','photo']

    widgets = {
      'photo':forms.FileInput(attrs={
        'id':'add-single-img',
      }),
      'gender':forms.CheckboxInput(attrs={
        'class':'form-check-input',
        'id':'gender-checkbox'
      })
    }

class GroupCreationForm(ModelForm):
  class Meta():
    model = Group
    fields = ["name"]


class UploadPhotoForm(forms.Form):
  image_field = forms.ImageField()