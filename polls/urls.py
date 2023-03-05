from django.urls import path
from . import views

#This App contains 4 URL : for showing list of all queries, for creating query, for sending comments, query/comment succesffuly sent 

urlpatterns = [
    path('',views.polls_home,name='polls'),
    path('create/',views.poll_create,name='poll_create'),
    path('view/',views.poll_view,name='poll_view'),
]