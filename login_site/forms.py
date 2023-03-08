from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#This is a form which extends on the UserCreationForm class (asked in sign up page)
#contains extra fields email, first_name, last_name, is_staff
class SignUpForm(UserCreationForm):

    address = forms.CharField(max_length=4,required=True)
    first_name = forms.CharField(max_length=20,required=True)
    last_name = forms.CharField(max_length=20,required=True)
    contact_number = forms.IntegerField(required=True)
    parent_name = forms.CharField(max_length=20,required=True)
    parent_contact = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "address", "contact_number", "parent_name", "parent_contact", "password1", "password2"]

class OTPForm(forms.Form):
    otp = forms.IntegerField(required=True)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(required=True,max_length=150)