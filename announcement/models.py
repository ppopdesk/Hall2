from django.db import models
import datetime
from login_site.models import UserProfile
# Create your models here.

#Model 1 : Database features for the Anouncements Made by Admin Users
class Announcement(models.Model) :
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    designation = models.CharField(max_length=300)
    announcement_heading = models.TextField(null=True)
    announcement = models.TextField(null=True)
    date = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return str(self.user.username) + ' ' + str(self.date)

#Model 2 : Database fields for the Events added by Admin Users
class Event(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    designation = models.CharField(max_length=300)
    event_date = models.DateField(null=True)
    event_time = models.TimeField(default=datetime.time.min)
    event_headline = models.CharField(null=True,max_length=150)

    def __str__(self):
        return self.user.username + ' ' + self.event_headline + ' ' + str(self.event_date)
