from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.home_view,name='home'),
    path('about/',views.about_view,name='about'),
    path('about/',views.mess_view,name='mess_about'),
]