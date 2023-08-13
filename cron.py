from guest_booking.models import Reservation, TemporaryUser

#Guest Booking CRONJOBS
def update_reservations():
    active_reservations = Reservation.objects.filter(is_active=True)
    for reservation in active_reservations:
        reservation.save()
    return None

