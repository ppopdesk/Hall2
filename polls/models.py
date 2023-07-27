from django.db import models
from login_site.models import UserProfile 
from datetime import date

# Create your models here.
class Poll(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    poll_created = models.DateField(default=date.today())
    poll_title = models.TextField(default='')
    poll_description = models.TextField(default=None)
    poll_question = models.CharField(blank=True,max_length=300)
    opt1 = models.CharField(default='Yes',max_length=300)
    opt2 = models.CharField(default='No',max_length=300)
    opt1_votes = models.IntegerField(default=0)
    opt2_votes = models.IntegerField(default=0)
    poll_deadline = models.DateField(default=None)

    def __str__(self):
        return self.username +' '+self.poll_title

class PollVotes(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    voter = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    opt1 = models.BooleanField(default=False)
    opt2 = models.BooleanField(default=False)

    def __str__(self):
        return self.voter.username + ' : ' + self.poll.poll_title