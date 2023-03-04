from django.db import models
from django.contrib.auth.models import User 
from datetime import date

# Create your models here.
class Poll(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    poll_created = models.DateField(default=date.today())
    poll_title = models.TextField(default='')
    poll_description = models.TextField(default=None)
    poll_question = models.CharField(blank=True,max_length=300)
    poll_upvotes = models.IntegerField(default=0)
    poll_downotes = models.IntegerField(default=0)
    poll_deadline = models.DateField(default=None)

    def __str__(self):
        return self.username +' '+self.poll_title

class PollVotes(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    voter = models.ForeignKey(User,on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def __str__(self):
        return self.voter.username + ' : ' + self.poll.poll_title