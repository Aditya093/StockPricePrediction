from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class CreateUseForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        widgets={
            'username':forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':"Username"
            }),
            'email':forms.EmailInput(attrs={
                'class':"form-control",
                'placeholder':"Email"
            }),
            'password1':forms.PasswordInput(attrs={
                'class':"form-control",
                'placeholder':"Password"
            }),
             'password2':forms.PasswordInput(attrs={
                'class':"form-control",
                'placeholder':"Confirm Password"
            }),
        }