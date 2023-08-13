from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RoomReservation, RoomReservationReferred
from django.contrib.auth.models import User
from .models import Reservation, Room
from userprofile.models import student_excel
from login_site.models import UserProfile
from django.http import HttpResponse
from datetime import date
from login_site.views import key_gen
from login_site.forms import OTPForm
from django.db.models import Q
from django.template.loader import render_to_string
from hall2temp.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, BadHeaderError
from datetime import date
from django.contrib import messages
import uuid
import pyotp
import base64

# Create your views here.

def redirect_view(request):
    try:
        if request.user.is_authenticated:
            return redirect('bookings')
        else:
            return redirect('guest_home')
    except:
        return redirect('guest_home')

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

@login_required
def room_reservation(request):
    if request.method == "POST":
        user = request.user
        form = RoomReservation(data = request.POST)
        if form.is_valid():
            data_dict = form.cleaned_data
            data_dict['guest'] = user
            if (data_dict['check_in'] < data_dict['check_out']) and (data_dict['check_in'] >= date.today()) and (data_dict['check_out'] > date.today()):
                if room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])):
                    room_id = int(room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])))
                    room = Room.objects.get(room_id = room_id)
                    data_dict['room'] = room
                    data_dict['is_active'] = True
                    if not Reservation.objects.filter(guest=user,is_active=True).exists():
                        obj = Reservation.objects.create(room = data_dict['room'], check_in = data_dict['check_in'],
                            check_out = data_dict['check_out'], guest = data_dict['guest'],
                            is_active = data_dict['is_active'], mobile_of_student = int(data_dict['mobile_of_student']),
                            address_of_student = data_dict['address_of_student'], mobile_of_guest = int(data_dict['mobile_of_guest']),
                            number_of_guests = int(data_dict['number_of_guests']))           
                        obj.save()
                        return HttpResponse(obj.reservation_id)
                    else:
                        return HttpResponse("A room already booked by this user")
                else:
                    if int(data_dict['room_preference']) !=0 :
                        return HttpResponse("Preferred room not available in these dates. Book another room or select the no preference option.")
                    return HttpResponse("No Rooms Available in these dates")
            else:
                return HttpResponse("Enter valid dates")  
        else:
            return HttpResponse("Form error") 
    else:
        form = RoomReservation()
    return render(request,"guest_booking/room_booking.html",{'form':form})

def referred_room_reservation(request):
    if request.method == "POST":
        form = RoomReservationReferred(data=request.POST)
        if form.is_valid():
            data_dict = form.cleaned_data
            roll_number = int(data_dict.get('roll_number_referred_student'))
            if UserProfile.objects.filter(username=roll_number).exists():
                referred_user = UserProfile.objects.get(username=roll_number)
                if (data_dict['check_in'] < data_dict['check_out']) and (data_dict['check_in'] >= date.today()) and (data_dict['check_out'] > date.today()):
                    if room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])):
                        room_id = int(room_availability(data_dict['check_in'],data_dict['check_out'],int(data_dict['room_preference'])))
                        room = Room.objects.get(room_id = room_id)
                        data_dict['room'] = room
                        if not Reservation.objects.filter(guest=referred_user,is_active=True).exists():
                            obj = Reservation.objects.create(room = data_dict['room'], check_in = data_dict['check_in'],
                                    check_out = data_dict['check_out'], roll_number_external_student = data_dict['roll_number_external_student'],
                                    name_external_student = data_dict['name_external_student'], guest = referred_user,
                                    mobile_of_student = int(data_dict['mobile_of_student']),
                                    referred_booking = True, address_of_student = data_dict['address_of_student'], 
                                    mobile_of_guest = int(data_dict['mobile_of_guest']),
                                    number_of_guests = int(data_dict['number_of_guests'])) 
                            obj.counter+=1
                            obj.save()
                        else:
                            return HttpResponse('This referee already has an active booking in his name')
                    else:
                        if int(data_dict['room_preference']) !=0 :
                            return HttpResponse("Preferred room not available in these dates. Book another room or select the no preference option.")
                        return HttpResponse("No Rooms Available in these dates")
                    id = obj.reservation_id
                    key = base64.b32encode(key_gen(id).encode()) 
                    OTP = pyotp.HOTP(key) 
                    subject = 'Referal Request for guest booking'
                    email_template_name = "guest_booking/guestbooking_mail.txt"
                    email = 'vijaya21@iitk.ac.in'
                    c = {'otp':OTP.at(obj.counter),'name':data_dict.get('name_external_student'),'roll_number':data_dict.get('roll_number_external_student')}
                    email_template = render_to_string(email_template_name, c)
                    send_mail(subject, email_template, EMAIL_HOST_USER, [email], fail_silently=False)
                    return redirect('otp_verify_guest_booking',booking_id = id)
                else:
                    return HttpResponse("Enter valid dates") 
            else:
                return render(request,"guest_booking/not_hall_resident_guest.html")
        else:
            return HttpResponse("Form Invalid")
    else:        
        form = RoomReservationReferred()
        q1 = Q(check_out__gte = date.today())
        q2 = Q(is_active = True)
        all_reservations = Reservation.objects.filter(q1 & q2).order_by('check_out')
        return render(request,"guest_booking/reference_booking_one.html",{'form':form,'reservations': all_reservations})

def otp_verify_guest_booking(request, booking_id):
    if request.method=='POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            otp_given = (data['otp'])
            reservation = Reservation.objects.get(reservation_id=booking_id)
            key = base64.b32encode(key_gen(booking_id).encode())
            OTP = pyotp.HOTP(key)
            if OTP.verify(otp_given,reservation.counter):
                reservation.is_active = True
                reservation.save()
                return HttpResponse(reservation.reservation_id)
            else:
                return HttpResponse("Wrong")
        else:
            return HttpResponse("Form Invalid")
    else:
        form = OTPForm()
    return render(request,'guest_booking/otp_enter_guest.html',{'form':form})

@login_required
def booking_success(request):
    return render(request,'guest_booking/booking_success.html')

def view_bookings(request):
    number_of_rooms = len(Room.objects.all())
    q1 = Q(check_out__gte = date.today())
    q2 = Q(is_active = True)
    all_reservations = Reservation.objects.filter(q1 & q2).order_by('check_out')
    return render(request,"guest_booking/current_bookings.html",{'reservations': all_reservations, 'number_of_rooms':number_of_rooms})

@login_required
def user_bookings(request):
    user = request.user
    active_reservations = Reservation.objects.filter(is_active=True, guest=user).order_by('check_in')
    past_reservations = Reservation.objects.filter(is_active=False, guest=user).order_by('check_in')
    return render(request,'guest_booking/user_bookings.html',{'active_reservations':active_reservations,'past_reservations':past_reservations})

def receipt(request):
    reservation_id = uuid.UUID(str(request.GET.get('id')))
    try:
        reservation = Reservation.objects.get(reservation_id=reservation_id)
        if reservation.is_active:
            return render(request,'guest_booking/receipt.html',{'reservation':reservation})
        else:
            return HttpResponse("This is not an active reservation")
    except:
        return HttpResponse("This is an invalid booking_id")
