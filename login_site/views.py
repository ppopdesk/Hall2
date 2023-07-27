from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm 
from .forms import SignUpForm, OTPForm, ForgotPasswordForm, CustomAuthForm
from django.contrib.auth import logout, update_session_auth_hash, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import math, random, secrets, string
from .models import UserProfile
from django.core.mail import send_mail, BadHeaderError
from hall2temp.settings import EMAIL_HOST_USER
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from userprofile.models import student_excel
import pyotp
from datetime import datetime
import base64

def key_gen(username):
        return str(username) + str(datetime.date(datetime.now())) + "kim"

def generatePassword():
    letters = string.ascii_letters
    digits = string.digits
    special_chars = string.punctuation
    alphabet = letters + digits + special_chars
    pwd = ''
    for i in range(10):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd

#View 0 : For handling error
def handler404(request, *args, **argv):
    return render(request,'404error.html')

#View 1 : To Sign Up a User according to the in built User model and the form defined in .forms
def sign_up_view(request):
    if request.method == "POST" :
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            roll_number = int(data.get('username'))
            email = 'vijaya21@iitk.ac.in'
            if student_excel.objects.filter(roll_number=roll_number).exists():
                user = form.save(commit=False)
                user.email = email
                user.is_active = False
                user.counter +=1
                user.save()
                key = base64.b32encode(key_gen(user.username).encode()) 
                OTP = pyotp.HOTP(key) 
                subject = 'Activate Your Account in Hall 2 website'
                email_template_name = "login_site/otp_mail.txt"
                c = {'otp':OTP.at(user.counter)}
                email_template = render_to_string(email_template_name, c)
                send_mail(subject, email_template, EMAIL_HOST_USER, [email], fail_silently=False)
                return redirect('otp_verify',username = user.username)
            else:
                return render(request,"login_site/not_hall_resident.html")
    else:
        form = SignUpForm()
    return render(request,"login_site/signup.html",{'form':form})

def otp_verify(request, username):
    if request.method=='POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            otp_given = data['otp']
            user_curr = UserProfile.objects.get(username=username)
            key = base64.b32encode(key_gen(user_curr.username).encode())
            OTP = pyotp.HOTP(key) 
            if OTP.verify(otp_given,user_curr.counter):
                user_curr.is_active = True
                user_curr.save()
                return HttpResponse("Success")
            else:
                return HttpResponse("Wrong")
        else:
            return HttpResponse("Form Invalid")
    else:
        form = OTPForm()
    return render(request,'login_site/otp_enter.html',{'form':form})

#View 2 : To Login a User who has already signed up. Upon succesful login it redirects to Profile page
def login_view(request):
    if request.method == "POST" :
        form = CustomAuthForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/userprofile/profile/')
    else:
        form = CustomAuthForm()
    return render(request,"login_site/login.html",{'form':form})

#View 3 : To log out a user who has already logged in
@login_required
def logout_view(request):
    logout(request)
    return render(request,'login_site/logout.html')

#View 4 : To change password of the user. Available in the login/signup page (!Doesnt make sense needs change)
@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            logout(request)
            return HttpResponse("Success")
        else:
            return HttpResponse("Error")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login_site/change_password.html', {'form': form})

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = ForgotPasswordForm(request.POST)
        if password_reset_form.is_valid():
            username = password_reset_form.cleaned_data['username']
            try:
                user = UserProfile.objects.get(username=username)
                subject = "Password Reset Requested"
                email_template_name = "login_site/password_reset_email.txt"
                c = {
				"email":user.email,
				'domain':'127.0.0.1:8000',
				'site_name': 'Hall 2',
				"uid": urlsafe_base64_encode(force_bytes(user.pk)),
				"user": user,
				'token': default_token_generator.make_token(user),
				'protocol': 'http',
				}
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, EMAIL_HOST_USER , [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponse("""We've emailed you instructions for setting your password, if an account exists with the username you entered. You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder.""")
            except:
                return HttpResponse('User doesnt exist')
    password_reset_form = ForgotPasswordForm()
    return render(request=request, template_name="login_site/password_reset_form.html", context={"password_reset_form":password_reset_form})
