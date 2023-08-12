from django.db import models
import datetime
from login_site.models import UserProfile
# Create your models here.

#Model 1 : Queries database
class Query(models.Model) :
  
    username = models.CharField(null=True,max_length=150)
    query = models.TextField(null=True)
    query_topic = models.CharField(default="Others",max_length=50)
    query_heading = models.CharField(default="Query",max_length=150)
    date = models.DateField(default=datetime.date.today)
    upvote_number = models.IntegerField(default=0)
    downvote_number = models.IntegerField(default=0)
    votes = models.ManyToManyField(UserProfile,default=None)
    
    def __str__(self):
        return self.username + ' ' + str(self.id) + ' ' + str(self.date)

#Model 2 : Comments database
class QueryResponse(models.Model):
    
    username = models.CharField(blank=False,max_length=150)
    response = models.TextField(blank=False)
    id_map = models.IntegerField(blank=False,default=0)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.username + ' ' + str(self.date)
