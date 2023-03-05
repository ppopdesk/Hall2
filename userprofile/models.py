from django.db import models
import datetime
# Create your models here.

class student(models.Model):
    name = models.CharField(max_length=200)
    roll_number = models.IntegerField()
    
    def __str__(self):
        return self.name + ' ' + str(self.roll_number)

class AnonymousComplaints(models.Model):
    query = models.TextField(null=True)
    query_topic = models.CharField(default="Others",max_length=50)
    query_heading = models.CharField(default="Query",max_length=150)
    date = models.DateField(default=datetime.date.today)