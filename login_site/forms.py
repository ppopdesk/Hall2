from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import UserProfile
from django.forms.widgets import PasswordInput, TextInput

#This is a form which extends on the UserCreationForm class (asked in sign up page)
#contains extra fields email, first_name, last_name, is_staff

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control','placeholder': 'Roll number'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=20,required=True)
    last_name = forms.CharField(max_length=20,required=True)
    hall_address = forms.CharField(max_length=4,required=True)
    contact_number = forms.IntegerField(required=True)
    parent_name = forms.CharField(max_length=30,required=True)
    parent_contact = forms.IntegerField(required=True)

    class Meta:
        model = UserProfile
        fields = ["username", "first_name", "last_name", "hall_address", "contact_number", "parent_name", "parent_contact",]

class UserChangeForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = ("username",)

class OTPForm(forms.Form):
    otp = forms.CharField(required=True)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(required=True,max_length=150)