from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RoomReservation
from .models import Reservation, Room
from django.http import HttpResponse
from datetime import date
from django.db.models import Q

# Create your views here.

def room_availability(check_in,check_out):
    condition_1 = Q(check_in__gte = check_in) & Q(check_in__lte = check_out) & Q(check_out__gte = check_out) #check_in of exisiting res in bw
    condition_2 = Q(check_in__lte = check_in) & Q(check_out__gte = check_out) #new res completely inside existing res
    condition_3 = Q(check_in__lte = check_in) & Q(check_out__lte = check_out) & Q(check_out__gte = check_in) #check_out of exisiting res in bw
    condition_4 = Q(check_in__gte = check_in) & Q(check_out__lte = check_out)
    condition_5 = Q(is_active = True)
    rooms_eliminated = Reservation.objects.filter((condition_5) & (condition_1 | condition_2 | condition_3 | condition_4))
    room_ids = []
    for room in rooms_eliminated:
        if room.room.room_id not in room_ids:
            room_ids.append(room.room.room_id)
    for room in Room.objects.all():
        if room.room_id not in room_ids:
            return room.room_id
    return None

@login_required
def room_reservation(request):
    if request.method == "POST":
        user = request.user
        form = RoomReservation(data = request.POST)
        if form.is_valid():
            data_dict = form.cleaned_data
            data_dict['guest'] = user
            if room_availability(data_dict['check_in'],data_dict['check_out']):
                room_id = int(room_availability(data_dict['check_in'],data_dict['check_out']))
                room = Room.objects.get(room_id = room_id)
                data_dict['room'] = room
                data_dict['is_active'] = True
                obj = Reservation.objects.create(room = data_dict['room'], check_in = data_dict['check_in'],
                                                check_out = data_dict['check_out'], guest = data_dict['guest'],
                                                is_active = data_dict['is_active'], mobile_of_student = data_dict['mobile_of_student'],
                                                address_of_student = data_dict['address_of_student'], mobile_of_resident = data_dict['mobile_of_resident'],
                                                number_of_guests = data_dict['number_of_guests'])           
                obj.save()
                return redirect('../booking_success/')
            else:
                return HttpResponse("No Rooms Available in these dates")   
    else:
        form = RoomReservation()
    return render(request,"room_booking.html",{'form':form})

@login_required
def booking_success(request):
    return render(request,'booking_success.html')

@login_required
def view_bookings(request):
    if request.method=="POST":
        form = RoomReservation(data = request.POST)
        if form.is_valid():
            data_dict = form.cleaned_data
            condition_1 = Q(check_in__gte = data_dict['check_in']) & Q(check_in__lte = data_dict['check_out']) & Q(check_out__gte = data_dict['check_out']) #check_in of exisiting res in bw
            condition_2 = Q(check_in__lte = data_dict['check_in']) & Q(check_out__gte = data_dict['check_out']) #new res completely inside existing res
            condition_3 = Q(check_in__lte = data_dict['check_in']) & Q(check_out__lte = data_dict['check_out']) & Q(check_out__gte = data_dict['check_in']) #check_out of exisiting res in bw
            condition_4 = Q(check_in__gte = data_dict['check_in']) & Q(check_out__lte = data_dict['check_out'])
            condition_5 = Q(is_active = True)
            relevent_reservations = Reservation.objects.filter((condition_5) & (condition_1 | condition_2 | condition_3 | condition_4)).order_by('check_out')
            availability = False
            if room_availability(data_dict['check_in'],data_dict['check_out']):
                availability = True
            return render(request, "relevant_bookings.html", {'relevant_reservations' : relevent_reservations, 'availability' : availability})
    else:
        form = RoomReservation()
        number_of_rooms = len(Room.objects.all())
        q1 = Q(check_out__gte = date.today())
        q2 = Q(is_active = True)
        all_reservations = Reservation.objects.filter(q1 & q2).order_by('check_out')
    return render(request,"current_bookings.html",{'reservations':all_reservations, 'number_of_rooms':number_of_rooms})

@login_required
def user_bookings(request):
    user = request.user
    active_reservations = Reservation.objects.filter(is_active=True, guest=user).order_by('check_in')
    past_reservations = Reservation.objects.filter(is_active=False, guest=user).order_by('check_in')
    return render(request,'user_bookings.html',{'active_reservations':active_reservations,'past_reservations':past_reservations})