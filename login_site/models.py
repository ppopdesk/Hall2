from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from datetime import datetime

username_validator = RegexValidator(r'^[0-9]*$','You can only enter digits')
#Create Models Here

class UserProfile(AbstractUser):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    hall_address = models.CharField(max_length=4,null=True)
    contact_number = models.IntegerField()
    parent_name = models.CharField(max_length=30,null=True)
    parent_contact = models.IntegerField(null=True)
    parent_contact = models.CharField(max_length=100,null=True)
    counter = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    designation = models.CharField(max_length=50, blank=True)

    REQUIRED_FIELDS = ['first_name','last_name','contact_number']

    def __str__(self):
        return self.username

UserProfile._meta.get_field('username').validators = [username_validator]
UserProfile._meta.get_field('username').help_text = "Required. Digits only"
