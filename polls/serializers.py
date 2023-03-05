from rest_framework import serializers
from .models import PollVotes, Poll

#All existing models have been serialized

class PollVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PollVotes
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Poll
        fields = '__all__'