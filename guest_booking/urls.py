from django.urls import path, re_path
from . import views

urlpatterns = [
    path('room_reservation/',views.room_reservation,name='room_reservation'),
    path('booking_success/',views.booking_success,name='booking_success'),
    path('bookings/',views.view_bookings,name='bookings'),
    path('userbookings/',views.user_bookings,name='user_bookings'),
    path('guest/',views.referred_booking,name='guest_home'),
    re_path(r'^otpverify/(?P<username>[\w.@+-]+)/$',views.otp_verify_guest_booking,name='otp_verify_guest_booking'),
    path('room_res_referred/',views.referred_room_reservation,name='referred_room_reservation'),
]