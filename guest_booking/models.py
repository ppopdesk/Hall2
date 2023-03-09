from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import date

# Create your models here.

class Room(models.Model):
    room_id = models.IntegerField(unique=True)
    def __str__(self):
        return 'Room ' + str(self.room_id)

class Reservation(models.Model):
    reservation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(User, on_delete= models.CASCADE,null=True)
    roll_number_booker = models.IntegerField() #make this unique
    mobile_of_student = models.IntegerField(default=' ')
    address_of_student = models.CharField(max_length=20, default=' ')
    mobile_of_guest = models.IntegerField(default=0)
    number_of_guests = models.IntegerField(default=0)
    roll_number_referred_student = models.IntegerField(null=True)
    name_referred_student = models.CharField(max_length=300,null=True)
    referred_booking = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active == True and self.check_out < date.today():
            self.is_active = False
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.roll_number_booker) + ' : ' + 'Room ' + str(self.room.room_id)

class TemporaryUser(models.Model):
    hall_user = models.OneToOneField(User,on_delete=models.CASCADE)
    roll_number_booker = models.IntegerField(primary_key=True)
    name_of_booker = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.roll_number_booker) + ' : ' + str(self.hall_user.username)