from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from hall2temp.settings import EMAIL_HOST_USER
from .forms import MailForm
from login_site.models import UserProfile
from .models import student_excel, AnonymousComplaints
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.http import HttpResponse

# Create your views here.

#View 1 : Shows Profile Page of the User upon login
@login_required
def profile_view(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    return render(request,"profile.html",{'user':user, 'profile':profile})

@login_required
def send_anon_complaint(request):
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            query_topic = str(data['query_topic'])
            query = str(data['query'])
            query_heading = str(data['query_heading'])
            complaint = AnonymousComplaints.objects.create(
                query=query,
                query_topic=query_topic,
                query_heading=query_heading)
            complaint.save()
            return HttpResponse("Success")
        else:
            return HttpResponse("Form Error")
    else:
        form = MailForm()
    return render(request,'send_anon_complaint.html',{'form':form})

@login_required
def anon_complaints_view(request):
    user = request.user
    if user.is_staff:
        complaints = AnonymousComplaints.objects.all().order_by('-id')
        return render(request,'anon_complaints_view.html',{'complaints' : complaints})
    else:
        return render(request,"404error.html")

def unique_complaint_view(request):
    id  = int(request.GET.get('id'))
    complaint_main = AnonymousComplaints.objects.get(id = id)
    return render(request, 'individual_complaint_view.html', {'complaint_main':complaint_main})

@login_required
def import_excel(request):
    if request.user.is_staff:
        if request.method == 'POST':
            if request.FILES.get('students_data'):    
                myfile = request.FILES['students_data']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                empexceldata = pd.read_excel(filename)    
                dbframe = empexceldata
                for dbframe in dbframe.itertuples():
                    obj = student_excel.objects.create(name=dbframe.name,roll_number=int(dbframe.roll_number))           
                    obj.save()
                return HttpResponse("Success")
            else:
                return HttpResponse("Please upload a file")
        else:
            return render(request, 'import_excel_db.html')
    else:
        return render(request,"404error.html")
