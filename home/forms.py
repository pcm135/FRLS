from django import forms
from .models import *
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm


class UserSignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Username'}
    ), required=True, max_length=50)

    email = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Enter your email'}
    ), required=True, max_length=50)

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Password'}
    ), required=True, max_length=50)

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control input-block', 'placeholder': 'Conform Password'}
    ), required=True, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    #
    # def clean_username(self):
    #     user = self.cleaned_data['username']
    #     try:
    #         match = User.objects.get(username=user)
    #     except:
    #         return self.cleaned_data['username']
    #     raise forms.ValidationError("Username already exist")
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     try:
    #         mt = validate_email(email)
    #     except:
    #         return forms.ValidationError("Incorrect email format")
    #     return email
    #
    # def clean_confirm_password(self):
    #     pass1 = self.cleaned_data['password']
    #     pass2 = self.cleaned_data['confirm_password']
    #     MAX_LEN = 8
    #     if pass1 and pass2:
    #         if pass1 != pass2:
    #             raise forms.ValidationError("Two passwords not same")
    #         else:
    #             if len(pass1) < MAX_LEN:
    #                 raise forms.ValidationError("Password should be %d characters" %MAX_LEN)
    #             if pass1.isdigit():
    #                 raise forms.ValidationError("Password should not all numeric")
    #
