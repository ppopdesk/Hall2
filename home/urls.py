from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home_view,name='home'),
    path('announcements/',views.announcement_view,name='announcements'),
]