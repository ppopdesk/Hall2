from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import UserProfile
from .forms import SignUpForm, UserChangeForm
# Register your models here.

class AdminProfile(UserAdmin):
    add_form = SignUpForm
    form = UserChangeForm
    model = UserProfile
    list_display = ["username","is_staff"]
    list_filter = ["is_staff","is_superuser"]
    search_fields = ["username"]
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email','designation')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login','date_joined')
        }),
        ('Additional info', {
            'fields': ( 'hall_address', 'parent_name','parent_contact')
        })
    )

admin.site.register(UserProfile,AdminProfile)
admin.site.unregister(Group)