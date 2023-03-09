from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RoomReservation, RoomSearch, ReferenceBooking, RoomReservationReferred
from django.contrib.auth.models import User
from .models import Reservation, Room, TemporaryUser
from userprofile.models import student_excel
from login_site.models import User_OTP
from django.http import HttpResponse, JsonResponse
from datetime import date
from login_site.views import generateOTP
from login_site.forms import OTPForm
from django.db.models import Q
from django.template.loader import render_to_string
from hall2temp.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
import json

# Create your views here.

def room_availability(check_in,check_out,room_preference):
    condition_1 = Q(check_in__gte = check_in) & Q(check_in__lte = check_out) & Q(check_out__gte = check_out) #check_in of exisiting res in bw
    condition_2 = Q(check_in__lte = check_in) & Q(check_out__gte = check_out) #new res completely inside existing res
    condition_3 = Q(check_in__lte = check_in) & Q(check_out__lte = check_out) & Q(check_out__gte = check_in) #check_out of exisiting res in bw
    condition_4 = Q(check_in__gte = check_in) & Q(check_out__lte = check_out)
    condition_5 = Q(is_active = True)
    condition_6 = Q(check_out__gte = date.today())
    rooms_eliminated = Reservation.objects.filter((condition_6) & (condition_5) & (condition_1 | condition_2 | condition_3 | condition_4))
    room_ids = []
    for room in rooms_eliminated:
        if room.room.room_id not in room_ids:
            room_ids.append(room.room.room_id)
    if room_preference==0:
        for room in Room.objects.all():
            if room.room_id not in room_ids:
                return room.room_id
    else:
        if room_preference not in room_ids:
            return room_preference
    return None

def delete_irrelevant_temp_users():
    for temp_user in TemporaryUser.objects.all():
        if not Reservation.objects.filter(roll_number_booker=temp_user.roll_number_booker, guest=None).exists():
            temp_user.delete()

@login_required
def room_reservation(request):
    if request.method == "POST":
        user = request.user
        form = RoomReservation(data = request.POST)
        if form.is_valid():
            data_dict = form.cleaned_data
            data_dict['guest'] = user
            if room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])):
                room_id = int(room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])))
                room = Room.objects.get(room_id = room_id)
                data_dict['room'] = room
                data_dict['is_active'] = True
                obj = Reservation.objects.create(room = data_dict['room'], check_in = data_dict['check_in'],
                    check_out = data_dict['check_out'], guest = data_dict['guest'], roll_number_booker = int(user.username),
                    is_active = data_dict['is_active'], mobile_of_student = int(data_dict['mobile_of_student']),
                    address_of_student = data_dict['address_of_student'], mobile_of_guest = int(data_dict['mobile_of_guest']),
                    number_of_guests = int(data_dict['number_of_guests']))           
                obj.save()
                return HttpResponse("Success")
            else:
                return HttpResponse("No Rooms Available in these dates")  
        else:
            return HttpResponse(form.errors) 
    else:
        form = RoomReservation()
    return render(request,"room_booking.html",{'form':form})

def referred_booking(request):
    if request.method == "POST":
        form = ReferenceBooking(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            roll_number = int(data.get('roll_number_referred_student'))
            if student_excel.objects.filter(roll_number=roll_number).exists():
                referred_user = User.objects.get(username=roll_number)
                temporary_user = TemporaryUser.objects.create(
                    hall_user = referred_user,
                    roll_number_booker = data.get('roll_number_booker'),
                    name_of_booker = data.get('name_of_booker'),
                )
                temporary_user.save()
                otp = generateOTP()
                user_otp = User_OTP(user=referred_user,email = referred_user.email ,otp_generated=otp)
                user_otp.save()
                subject = 'Referal Request for guest booking'
                email_template_name = "guestbooking_mail.txt"
                email = 'vijaya21@iitk.ac.in'
                c = {'otp':otp,'name':data.get('name_of_booker'),'roll_number':data.get('roll_number_booker')}
                email_template = render_to_string(email_template_name, c)
                send_mail(subject, email_template, EMAIL_HOST_USER, [email], fail_silently=False)
                return redirect('otp_verify_guest_booking',username = referred_user.username)
            else:
                return render(request,"not_hall_resident_guest.html")
    else:        
        delete_irrelevant_temp_users()
        form = ReferenceBooking()
        q1 = Q(check_out__gte = date.today())
        q2 = Q(is_active = True)
        all_reservations = Reservation.objects.filter(q1 & q2).order_by('check_out')
    return render(request,"reference_booking_one.html",{'form':form,'reservations': all_reservations})

def otp_verify_guest_booking(request, username):
    if request.method=='POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            otp_given = int(data['otp'])
            user_curr = User.objects.get(username=username)
            otp_required = User_OTP.objects.get(user = user_curr).otp_generated
            if otp_given == otp_required:
                temp_user = TemporaryUser.objects.get(hall_user=user_curr)
                temp_user.is_active = True
                temp_user.save()
                user_otp = User_OTP.objects.get(user=user_curr)
                user_otp.delete()
                return HttpResponse(temp_user.roll_number_booker)
            else:
                return HttpResponse("Wrong")
        else:
            return HttpResponse("Form Invalid")
    else:
        form = OTPForm()
    return render(request,'otp_enter_guest.html',{'form':form})

def referred_room_reservation(request):
    if request.method == "POST":
        form = RoomReservationReferred(data = request.POST)
        if form.is_valid():
            data_dict = form.cleaned_data
            roll_number_booker = int(data_dict['roll_number_booker'])
            if TemporaryUser.objects.filter(roll_number_booker=roll_number_booker).exists() and TemporaryUser.objects.get(roll_number_booker=roll_number_booker).is_active:
                if room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])):
                    room_id = int(room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])))
                    room = Room.objects.get(room_id = room_id)
                    data_dict['room'] = room
                    data_dict['is_active'] = True
                    obj = Reservation.objects.create(room = data_dict['room'], check_in = data_dict['check_in'],
                            check_out = data_dict['check_out'], roll_number_booker = roll_number_booker,
                            is_active = data_dict['is_active'], mobile_of_student = int(data_dict['mobile_of_student']),
                            referred_booking = True, roll_number_referred_student = data_dict['roll_number_referred_student'],
                            name_referred_student = data_dict['name_referred_student'],
                            address_of_student = data_dict['address_of_student'], mobile_of_guest = int(data_dict['mobile_of_guest']),
                            number_of_guests = int(data_dict['number_of_guests'])) 
                    obj.save()
                    temp_user = TemporaryUser.objects.get(roll_number_booker=roll_number_booker)
                    temp_user.is_active = False
                    temp_user.save()
                    return HttpResponse("Success")
                else:
                    return HttpResponse("No Rooms Available in these dates")
            else:
                return HttpResponse("You are not eligible for booking")
        else:
            return HttpResponse(form.errors)
    else:
        roll_number_booker  = int(request.GET.get('roll_number_booker'))
        if TemporaryUser.objects.filter(roll_number_booker=roll_number_booker).exists() and TemporaryUser.objects.get(roll_number_booker=roll_number_booker).is_active:
            guest_booker = TemporaryUser.objects.get(roll_number_booker=roll_number_booker)
            form = RoomReservationReferred()
        else:
            return HttpResponse("You are not eligible for booking")
    return render(request,"guest_booking_outsider.html",{'form':form,'guest_booker':guest_booker})

@login_required
def booking_success(request):
    return render(request,'booking_success.html')

def view_bookings(request):
    if request.method=="POST":
        form = RoomSearch(data = request.POST)
        if form.is_valid():
            data_dict = form.cleaned_data
            if data_dict['room_preference'] != 0:
                room_preferred = Room.objects.get(room_id=int(data_dict['room_preference']))
                condition_0 = Q(room=room_preferred)
            else:
                condition_0 = ~Q(pk__in=[])
            condition_1 = Q(check_in__gte = data_dict['check_in']) & Q(check_in__lte = data_dict['check_out']) & Q(check_out__gte = data_dict['check_out']) #check_in of exisiting res in bw
            condition_2 = Q(check_in__lte = data_dict['check_in']) & Q(check_out__gte = data_dict['check_out']) #new res completely inside existing res
            condition_3 = Q(check_in__lte = data_dict['check_in']) & Q(check_out__lte = data_dict['check_out']) & Q(check_out__gte = data_dict['check_in']) #check_out of exisiting res in bw
            condition_4 = Q(check_in__gte = data_dict['check_in']) & Q(check_out__lte = data_dict['check_out'])
            condition_5 = Q(is_active = True) 
            condition_6 = Q(check_out__gte = date.today())
            relevent_reservations = Reservation.objects.filter((condition_0) & (condition_5) & (condition_1 | condition_2 | condition_3 | condition_4) &(condition_6)).order_by('check_out').values()
            availability = False
            if room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])):
                availability = True
            return JsonResponse({'relevent_reservations':list(relevent_reservations)})
    else:
        number_of_rooms = len(Room.objects.all())
        q1 = Q(check_out__gte = date.today())
        q2 = Q(is_active = True)
        all_reservations = Reservation.objects.filter(q1 & q2).order_by('check_out')
        return render(request,"current_bookings.html",{'reservations': all_reservations, 'number_of_rooms':number_of_rooms})

@login_required
def user_bookings(request):
    user = request.user
    active_reservations = Reservation.objects.filter(is_active=True, guest=user).order_by('check_in')
    past_reservations = Reservation.objects.filter(is_active=False, guest=user).order_by('check_in')
    return render(request,'user_bookings.html',{'active_reservations':active_reservations,'past_reservations':past_reservations})
