from django.urls import path
from . import views

#This App contains 1 URL : for showing profile page of user

urlpatterns = [
    path('profile/',views.profile_view ,name='profile'),
    path('mailhec/',views.send_anon_complaint,name='send_anon_complaint'),
    path('student_data/',views.import_excel,name='student_data'),
    path('anon_complaints/',views.anon_complaints_view,name='anon_complaints_view'),
    path('anon_complaint/',views.unique_complaint_view,name='unique_complaint_view'),
]