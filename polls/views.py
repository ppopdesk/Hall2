from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import PollCreationForm
from .models import PollVotes, Poll
from .serializers import PollSerializer, PollVotesSerializer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from django.http import JsonResponse   
from django.urls import reverse

# Create your views here.
@login_required
def polls_home(request):
    active_polls = Poll.objects.filter(poll_deadline__gte = date.today()).order_by('-id')
    past_polls = Poll.objects.filter(poll_deadline__lt = date.today()).order_by('-id')
    user = request.user
    return render(request,'polls/poll_home.html',{'active_polls' : active_polls, 'past_polls':past_polls, 'user':user})

@login_required
def poll_create(request):
    user = request.user
    if user.is_staff:
        if request.method == "POST":
            form = PollCreationForm(request.POST)
            if form.is_valid():
                data_dict = form.cleaned_data
                data_dict['username'] = user.username
                data_dict['email'] = user.email
                serializer = PollSerializer(data = data_dict)
                if serializer.is_valid():
                    serializer.save()
                    return redirect('../')
                else:
                    return HttpResponse("Error")
            else:
                return HttpResponse("Wrong Form")
        else:
            form = PollCreationForm()
        return render(request,"polls/poll_create.html",{'form':form})
    else:
        HttpResponse("404 Error")

@login_required
def poll_view(request):
    user = request.user
    if request.method == 'POST':
        voter = user
        opt1 = bool(int(request.POST.get('opt1')))
        opt2 = bool(int(request.POST.get('opt2')))
        id = int(request.POST.get('id'))
        poll = Poll.objects.get(id=id)
        data_dict = {
            'poll' : poll,
            'voter' : voter,
            'opt1' : opt1,
            'opt2' : opt2,
            }
        if PollVotes.objects.filter(voter=voter,poll=poll):
            return HttpResponse("Oops, seems like you have already voted")
        vote = PollVotes.objects.create(
            poll = data_dict['poll'],
            voter = data_dict['voter'],
            opt1 = data_dict['opt1'],
            opt2 = data_dict['opt2'],
        )
        vote.save()
        if opt1:
            opt1 = poll.opt1_votes+1
            poll.opt1_votes = opt1
            poll.save()
            return HttpResponse("Thank you for voting!")    
        elif opt2:
            opt2 = poll.opt2_votes+1
            poll.opt2_votes = opt2
            poll.save()
            return HttpResponse("Thank you for voting!") 
    id  = int(request.GET.get('id'))
    poll = Poll.objects.get(id = id)
    user_vote_status = PollVotes.objects.filter(voter=user,poll=poll).exists()
    active = True
    opt1percentage = 0
    opt2percentage = 0
    if poll.poll_deadline < date.today():
        active = False
        opt1percentage = int(100*((poll.opt1_votes)/(poll.opt1_votes+poll.opt2_votes)))
        opt2percentage = 100 - opt1percentage
    return render(request, 'polls/poll_view.html', {'poll':poll, 'active':active, 'user':user, 'user_vote_status':user_vote_status, 'opt1percentage':opt1percentage,'opt2percentage':opt2percentage})