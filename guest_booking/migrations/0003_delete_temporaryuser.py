# Generated by Django 4.2.3 on 2023-07-25 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guest_booking', '0002_alter_temporaryuser_hall_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TemporaryUser',
        ),
    ]
