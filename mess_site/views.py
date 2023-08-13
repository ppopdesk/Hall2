from django.shortcuts import render, redirect
from .models import MessMain, MessExtras, ExtrasOrder
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MessExtrasSerializer,MessMainSerializer, ExtrasOrderSerializer
import datetime
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth.models import User
import datetime


# Create your views here.

def time_of_day():
    now = datetime.datetime.now()
    #breakfast extras period 7am-9:30am
    if datetime.time(7) <= now.time() <= datetime.time(11, 30):
        return "Breakfast"
    
    #lunch extras period 12pm - 14:30pm
    elif datetime.time(12) <= now.time() <= datetime.time(14, 30):
        return "Lunch"
    
    #dinner extras period 19pm - 21:30pm
    elif datetime.time(19) <= now.time() <= datetime.time(21, 30):
        return "Dinner"

    return None

#View 1 : Mess Homepage which shows various options based on user status
@login_required
def mess_home(request):
    user = request.user
    return render(request,'mess_site/mess_home.html',{'user':user})


#View 5 : Can and only be seen by students and they can order extras here 
@login_required
def order_extras(request):
    user = request.user
    if not user.is_staff:
        extras = MessExtras.objects.all()
        if request.method == "POST":
            username = user.username
            email = user.email
            ordered_ids = request.POST.getlist('order')
            extras_items = []
            for id in ordered_ids:
                extras_items.append(MessExtras.objects.get(id = int(id)))
            order_date = datetime.date.today()
            order_month = datetime.datetime.now().month
            extra_order = ExtrasOrder.objects.create(username = username, email = email, order_date = order_date, order_month=order_month)
            for item in extras_items:
                extra_order.item_map.add(item)
            return redirect('extraadded',key_id = extra_order.id)
        type_of_meal = time_of_day()
        if type_of_meal:
            extras = MessExtras.objects.filter(extras_type__in = ["Permanent",type_of_meal], extras_day = datetime.datetime.now().strftime('%A'))
            return render(request,'mess_site/extras_order.html', {'extras':extras})
        else:
            return render(request,'mess_site/extras_order.html', {'extras':None})
    else:
        return render(request,"404error.html")

#View 6 : Displayed after extras have been ordered
@login_required
def extra_added(request, key_id):
    user = request.user
    if not user.is_staff:
        order = ExtrasOrder.objects.get(id = key_id)
        return render(request,"mess_site/add_extra_success.html",{'order':order})
    else:
        return render(request,"404error.html")

@login_required
def user_dues_view(request):
    if request.user.is_staff != True:
        user = request.user
        user_dues = ExtrasOrder.objects.filter(username=user.username).values('order_month').annotate(total = Sum('item_map__extras_price')).order_by('-order_month')
        return render(request, 'mess_site/dues_list.html', {'user_dues':user_dues})
    else:
        return render(request,"404error.html")

#View 7 : Can only be seen by the mess manager and he can add extra and main menu items
@api_view(['GET','POST'])
def manager_view(request):
    if request.user.is_staff == True:
        if request.method == "POST":
            post_data = request.data
            if int(post_data["main"]) == 0:
                data_dict = {
                    "extras_name" : post_data["extras_name"], 
                    "extras_price" : post_data["extras_price"], 
                    "extras_type" : post_data["extras_type"], 
                    "extras_day" : post_data["extras_day"],
                    "extras_quantity" : int(post_data["extras_quantity"])}
                serializer = MessExtrasSerializer(data = data_dict)
            else:
                data_dict = {
                "main_item_name" : post_data["main_item_name"],
                "day_of_the_week" : post_data["day_of_the_week"], 
                "type_of_meal" : post_data["type_of_meal"],}
                serializer = MessMainSerializer(data = data_dict)
            if serializer.is_valid():
                serializer.save()
                return redirect('/mess_site/')
        return render(request,'mess_site/manager.html')
    else:
        return render(request,"404error.html")

@login_required
def student_dues(request):
    if request.user.is_staff == True:
        if request.method == "POST":
            username = str(request.POST.get('username'))
            user_dues = ExtrasOrder.objects.filter(username=username).values('order_month').annotate(total = Sum('item_map__extras_price')).order_by('-order_month')
            return render(request, 'dues_list.html', {'user_dues':user_dues})
        return render(request,'mess_site/view_all_dues.html')
    return render(request,"404error.html")

@login_required
def student_orders(request):
    if request.user.is_staff == True:
        if request.method == "POST":
            username = str(request.POST.get('username'))
            orders = ExtrasOrder.objects.filter(username = username)
            student = User.objects.get(username = username)
            return render(request, 'mess_site/order_of_particular_student.html', {'orders':orders, 'student':student})
        return render(request,'mess_site/student_orders.html')
    return render(request,"404error.html")