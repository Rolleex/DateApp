from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(label='Емейл',
                             widget=forms.EmailInput(attrs={'class': 'form-control', }))
    password1 = forms.CharField(label='Пароль', max_length=25,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', }))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', }))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


# Создаем Юзера для хранения пароля и авторизации по email

class ProfileRegisterForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=(('Мужчина', 'male'), ('Женщина', 'female')))

    class Meta:
        model = Profile
        exclude = ['email', 'login']

# Форма заполнения данных профиля
# При регистрации автоматически зхаполним поля email и login
