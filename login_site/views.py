from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm 
from .forms import SignUpForm
from django.contrib.auth import logout, update_session_auth_hash, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMessage

#View 0 : For handling error
def handler404(request, *args, **argv):
    return render(request,'404error.html')

#View 1 : To Sign Up a User according to the in built User model and the form defined in .forms
def sign_up_view(request):
    if request.method == "POST" :
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            """user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()"""
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request,"login.html",{'form':form})

#View 2 : To Login a User who has already signed up. Upon succesful login it redirects to Profile url
def login_view(request):
    if request.method == "POST" :
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/userprofile/profile/')
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{'form':form})

#View 3 : To log out a user who has already logged in
@login_required
def logout_view(request):
    logout(request)
    return render(request,'logout.html')

#View 4 : To change password of the user. Available in the login/signup page !Doesnt make sense needs change
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})