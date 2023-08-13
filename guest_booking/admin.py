from django.contrib import admin
from .models import Room, Reservation
# Register your models here.
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ["guest", "room", "is_active", "referred_booking"]
    list_filter = ["is_active","referred_booking"]
    search_fields = ["guest"]
    exclude = ('counter',)

admin.site.register(Room)
admin.site.register(Reservation,ReservationAdmin)