from django.contrib import admin

# Register your models here.
from .models import Poll, PollVotes
admin.site.register(Poll)
admin.site.register(PollVotes)