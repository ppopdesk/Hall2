# Generated by Django 4.1.2 on 2023-03-04 15:06

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
            field=models.DateField(default=datetime.date(2023, 3, 4)),
        ),
    ]
