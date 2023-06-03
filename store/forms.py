from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import User, Product, Profile
from django import forms
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True


# form for the registration of a user
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


# form for applying changes to the customers user data
class CustomUserChangeForm(UserChangeForm):
    password = None
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Username'}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter Email-Address'}))

    class Meta:
        model = User
        fields = ['username', 'email']


# form for changing the password associated with a user
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Altes Passwort",
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control my-2', 'type': 'password'}))
    new_password1 = forms.CharField(label="Neues Passwort",
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control my-2', 'type': 'password'}))
    new_password2 = forms.CharField(label="Neues Passwort bestätigen",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control my-2', 'type': 'password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


# form for changing the profile picture associted with a user's profile
class ProfilePictureChangeForm(forms.ModelForm):
    profile_picture = forms.ImageField(label="Profile picture")

    class Meta:
        model = Profile
        fields = ('profile_picture', )
