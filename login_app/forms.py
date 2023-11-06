from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MinLengthValidator
from .validators import custom_password_validation
from login_app.models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'This email address is already in use.')
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        custom_password_validation(password1)  # Use your custom password validation
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")
        custom_password_validation(password2)  # Use your custom password validation
        return password2

class ThemeForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['theme']