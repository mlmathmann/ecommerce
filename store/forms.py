from django.contrib.auth.forms import UserCreationForm
from .models import User, Product
from django import forms


class CustomUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Username'}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Email-Address'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Password again'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProductStyleFilterForm(forms.Form):
    # name = forms.CharField()
    name = forms.ChoiceField(choices=Product.StyleChoices.choices)


