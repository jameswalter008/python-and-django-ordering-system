from django.db.models import fields
from django.forms import ModelForm
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm #built-in form
from django.contrib.auth.models import User #built-in model


class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields='__all__'

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

