from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['belong_to'].empty_label = "Категория не выбрана"

    class Meta:
        model = Page
        fields = ['title', 'slug', 'content', 'is_published', 'belong_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Заголовок',
                                            'style': 'width: 74%; margin-left: auto; display: block;'}),
            "slug": forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'URL',
                                           'style': 'width: 74%; margin-right: auto; display: block;'}),
            "content": forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Текст',
                                             'style': 'width: 75%; margin-left: auto; margin-right: auto; display: block;'}),
            "is_published": forms.CheckboxInput(attrs={'class': 'form-input'}),
            "belong_to": forms.Select(attrs={'class': 'form-input',
                                             'style': 'width: 75%; margin-left: auto; margin-right: auto; display: block;'}),
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Имя',
               'style': 'width: 75%; margin-left: auto; margin-right: auto; display: block;'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Электронная почта',
               'style': 'width: 75%; margin-left: auto; margin-right: auto; display: block;'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Пароль',
               'style': 'width: 75%; margin-left: auto; margin-right: auto; display: block;'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Повторите пароль',
               'style': 'width: 75%; margin-left: auto; margin-right: auto; display: block;'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Имя',
               'style': 'width: 75%; margin-left: auto; margin-right: auto; display: block;'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Пароль',
               'style': 'width: 75%; margin-left: auto; margin-right: auto; display: block;'}))

    class Meta:
        model = User
        fields = ('username', 'password')