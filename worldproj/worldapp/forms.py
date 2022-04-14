from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

from django.views.generic import UpdateView

from .models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['countrycode'].empty_label = "Country not selected"
        self.fields['countrycode'].widget.attrs['style'] = 'width:170px; height:25px';

    class Meta:
        model = City
        fields = ['name', 'countrycode', 'district', 'population']
        widgets = {
            #'name': forms.TextInput(attrs={'class': 'form-input'}),
            #'population': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 200:
            raise ValidationError('Длина превышает 200 символов')
        if not re.fullmatch(r'[a-zA-Z-\s()]+', name):
            raise ValidationError('Недопустиме символы')
        return name

    def clean_district(self):
        district = self.cleaned_data['district']
        if len(district) > 200:
            raise ValidationError('Длина превышает 200 символов')
        if not re.fullmatch(r'[a-zA-Z-\s()]+', district):
            raise ValidationError('Недопустиме символы')
        return district


class UpdatePostForm(AddPostForm):
    def is_valid(self):
        pass

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = User  # такая таблица есть в бд
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()


class FilterForm(forms.Form):
    part_name = forms.CharField(label='Name', max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'part name'}))
    min_population = forms.IntegerField(label='Min',  required=False, widget=forms.NumberInput(attrs={'placeholder': 'min population'}))
    max_population = forms.IntegerField(label='Max',  required=False, widget=forms.NumberInput(attrs={'placeholder': 'max population'}))
