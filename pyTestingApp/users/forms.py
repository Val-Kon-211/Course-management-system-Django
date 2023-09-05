from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput
from .models import Profile

class UserRegisterForm(UserCreationForm):
    username    = forms.CharField(label=u'Короткое имя пользователя')
    first_name  = forms.CharField(label=u'Имя')
    last_name   = forms.CharField(label=u'Фамилия')
    password1   = forms.CharField(label=u'Пароль', widget=PasswordInput)
    password2   = forms.CharField(label=u'Подтверждение пароля', widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']