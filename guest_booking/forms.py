from django import forms

class RoomReservationReferred(forms.Form):
    check_in = forms.DateField(required=True)
    check_out = forms.DateField(required=True)
    room_preference = forms.IntegerField(initial=0)
    number_of_guests = forms.IntegerField(required=True)
    mobile_of_student = forms.IntegerField(required=True)
    address_of_student = forms.CharField(max_length=20,required=True)
    mobile_of_guest = forms.IntegerField(required=True)
    roll_number_external_student = forms.IntegerField(required=True)
    name_external_student = forms.CharField(max_length=300,required=True)
    roll_number_referred_student = forms.IntegerField(required=True)
    name_referred_student = forms.CharField(max_length=300,required=True)

class RoomReservation(forms.Form):
    check_in = forms.DateField(required=True)
    check_out = forms.DateField(required=True)
    room_preference = forms.IntegerField(initial=0)
    number_of_guests = forms.IntegerField(required=True)
    mobile_of_student = forms.IntegerField(required=True)
    address_of_student = forms.CharField(max_length=20,required=True)
    mobile_of_guest = forms.IntegerField(required=True)

class RoomSearch(forms.Form):
    check_in = forms.DateField(required=True)
    check_out = forms.DateField(required=True)
    room_preference = forms.IntegerField(required=True)