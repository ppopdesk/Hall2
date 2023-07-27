from django.db import models
from login_site.models import UserProfile
import uuid
from datetime import date

# Create your models here.

class Room(models.Model):
    room_id = models.IntegerField(unique=True)
    def __str__(self):
        return 'Room ' + str(self.room_id)

class Reservation(models.Model):

    reservation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    guest = models.ForeignKey(UserProfile, on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    mobile_of_student = models.IntegerField(default=' ')
    address_of_student = models.CharField(max_length=20, default=' ')
    mobile_of_guest = models.IntegerField(default=0)
    number_of_guests = models.IntegerField(default=0)
    referred_booking = models.BooleanField(default=False)
    roll_number_external_student = models.IntegerField(null=True,blank=True)
    name_external_student = models.CharField(max_length=300,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    counter = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.is_active == True and self.check_out < date.today():
            self.is_active = False
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        if not self.referred_booking:
            return str(self.guest.username) + ' : ' + 'Room ' + str(self.room.room_id) + ' active : ' + str(self.is_active)
        else:
            return str(self.roll_number_external_student) + ' : ' + 'Room ' + str(self.room.room_id) + ' active : ' + str(self.is_active)
