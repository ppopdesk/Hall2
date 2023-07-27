from django.shortcuts import render, redirect
from .models import Announcement, Event
from .serializers import AnnouncementSerializer, EventSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from .forms import AnnouncementForm, EventForm
from django.contrib.auth.models import User
from login_site.models import UserProfile
from django.http import HttpResponse
# Create your views here.

#View 1 : Makes announcement based on form
@login_required
def make_announcement(request):
    user = request.user
    if user.is_staff:
        if request.method == "POST":
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                data_dict = form.cleaned_data
                data_dict['user'] = user
                profile = UserProfile.objects.get(user=user)
                data_dict['designation'] = profile.designation
                new_announcement = Announcement.objects.create(
                    user=user,designation = data_dict['designation'],
                    announcement = data_dict['announcement'],
                    announcement_heading = data_dict['announcement_heading'])
                new_announcement.save()
                return HttpResponse('Success')
            else:
                return HttpResponse(form.errors)
        return render(request,"announcement/send_announcement.html")
    else:
        return HttpResponse("404")

#View 2 : Makes event based on form 
@login_required
def add_event(request):
    user = request.user
    if user.is_staff:
        if request.method == "POST":
            form = EventForm(request.POST)
            if form.is_valid():
                data_dict = form.cleaned_data
                data_dict['user'] = user
                profile = UserProfile.objects.get(user=user)
                data_dict['designation'] = profile.designation
                serializer = EventSerializer(data = data_dict)
                if serializer.is_valid():
                    serializer.save()
                    return HttpResponse('Success')
            else:
                return HttpResponse(form.errors)
        return render(request,"announcement/send_event.html")
    else:
        return HttpResponse("404")