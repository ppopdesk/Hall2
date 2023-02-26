from django import forms

class RoomReservation(forms.Form):
    check_in = forms.DateField(required=True)
    check_out = forms.DateField(required=True)
