from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from .forms import SignUpForm, UserChangeForm
# Register your models here.

class AdminProfile(UserAdmin):
    add_form = SignUpForm
    form = UserChangeForm
    model = UserProfile
    list_display = ["username",]

admin.site.register(UserProfile,AdminProfile)