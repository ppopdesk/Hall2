from django.urls import path
from . import views

urlpatterns = [
    path('room_reservation/',views.room_reservation,name='room_reservation'),
    path('booking_success/',views.booking_success,name='booking_success'),
    path('bookings/',views.view_bookings,name='bookings'),
    path('userbookings/',views.user_bookings,name='user_bookings'),
]