# Generated by Django 4.2.3 on 2023-07-24 20:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='poll_created',
            field=models.DateField(default=datetime.date(2023, 7, 25)),
        ),
    ]
