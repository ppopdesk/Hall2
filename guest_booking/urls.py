from django.urls import path, re_path
from . import views

urlpatterns = [
    path('',views.redirect_view,name='guest_base'),
    path('room_reservation/',views.room_reservation,name='room_reservation'),
    path('booking_success/',views.booking_success,name='booking_success'),
    path('bookings/',views.view_bookings,name='bookings'),
    path('userbookings/',views.user_bookings,name='user_bookings'),
    path('guest/',views.referred_room_reservation,name='guest_home'),
    path('otpverify/<uuid:booking_id>/$',views.otp_verify_guest_booking,name='otp_verify_guest_booking'),
    path('receipt/',views.receipt,name='receipt'),
]