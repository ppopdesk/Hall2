from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

#Create Models Here

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=4)
    contact_number = models.IntegerField()
    parent_name = models.CharField(max_length=20)
    parent_contact = models.IntegerField()
    designation = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username + ' ' + self.user.email

class User_OTP(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    email = models.EmailField(null=True,max_length=50)
    otp_generated = models.IntegerField(null=True)

    def __str__(self):
        return str(self.user) + ' ' + str(datetime.now())
