from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'photo', 'content', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        else:
            return title

    def clean_is_published(self):
        is_published = self.cleaned_data['is_published']
        if not is_published:
            raise ValidationError('Статья обязательно должна быть опубликована')
        else:
            return is_published


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=155, label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password1 = forms.CharField(max_length=25, label="Придумайте пароль", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=25, label="Повторите пароль", widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=155, label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autofocus': 'autofocus'}))
    password = forms.CharField(max_length=25, label='Введите пароль', widget=forms.PasswordInput(
        {'class': 'form-control'}))


class ContactForm(forms.Form):
    subject = forms.CharField(label="Тема письма", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()