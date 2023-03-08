from django.contrib import admin
from .models import Room, Reservation, TemporaryUser
# Register your models here.

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(TemporaryUser)