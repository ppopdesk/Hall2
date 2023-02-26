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
    guest = models.ForeignKey(User, on_delete= models.CASCADE)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active == True and self.check_out < date.today():
            self.is_active = False
        super(Reservation, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.guest.username) + ' : ' + 'Room ' + str(self.room_id)