from django import forms

class RoomReservation(forms.Form):
    check_in = forms.DateField(required=True)
    check_out = forms.DateField(required=True)
    number_of_guests = forms.IntegerField()
    mobile_of_student = forms.IntegerField()
    address_of_student = forms.CharField(max_length=20)
    mobile_of_guest = forms.IntegerField