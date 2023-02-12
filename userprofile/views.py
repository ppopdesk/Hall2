from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from hall2temp.settings import EMAIL_HOST_USER
from .forms import MailForm
from .models import student
from django.core.files.storage import FileSystemStorage
import pandas as pd
# Create your views here.

#View 1 : Shows Profile Page of the User upon login
@login_required
def profile_view(request):
    user = request.user
    return render(request,"profile.html",{'user':user})

@login_required
def mail_hec(request):
    user = request.user
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = str(data['subject'])
            body = str(data['body'])
            recepient_mail = 'sunrockers8@gmail.com'
            send_mail(subject,body,EMAIL_HOST_USER,[recepient_mail],fail_silently=False)
            return redirect('../mail_sent/')
    else:
        form = MailForm()
    return render(request,'send_mail.html',{'form':form})

def mail_sent(request):
    return render(request,'formsent.html')

@login_required
def import_excel(request):
    if request.user.is_staff:
        if request.method == 'POST' and request.FILES['students_data']:      
            myfile = request.FILES['students_data']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            empexceldata = pd.read_excel(filename)    
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():
                obj = student.objects.create(name=dbframe.name,roll_number=int(dbframe.roll_number))           
                obj.save()
            return redirect('../formsent/')
        return render(request, 'import_excel_db.html')
    else:
        return render(request,"404error.html")

def form_sent_view(request):
    return render(request,"formsent.html")