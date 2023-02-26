from django.urls import path
from . import views

#This App contains 1 URL : for showing profile page of user

urlpatterns = [
    path('profile/',views.profile_view ,name='profile'),
    path('mailhec/',views.mail_hec,name='mail_hec'),
    path('mail_sent/',views.mail_sent,name='mail_sent'),
    path('student_data/',views.import_excel,name='student_data'),
    path('formsent/',views.form_sent_view,name='form_sent'),
]