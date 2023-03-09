from django.urls import path, re_path
from . import views

urlpatterns = [
    path('home/',views.home_view,name='home'),
    path('about/',views.about_view,name='about'),
    path('mess/',views.mess_view,name='mess_about'),
    path('facilities/',views.facilities_view,name='facilities'),
]