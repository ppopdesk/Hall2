# Generated by Django 4.1.2 on 2023-03-07 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest_booking', '0003_alter_reservation_guest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='mobile_of_guest',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='number_of_guests',
            field=models.IntegerField(default=0),
        ),
    ]
