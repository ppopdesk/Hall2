# Generated by Django 4.2.3 on 2023-07-23 21:57

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=150)),
                ('poll_created', models.DateField(default=datetime.date(2023, 7, 24))),
                ('poll_title', models.TextField(default='')),
                ('poll_description', models.TextField(default=None)),
                ('poll_question', models.CharField(blank=True, max_length=300)),
                ('opt1', models.CharField(default='Yes', max_length=300)),
                ('opt2', models.CharField(default='No', max_length=300)),
                ('opt1_votes', models.IntegerField(default=0)),
                ('opt2_votes', models.IntegerField(default=0)),
                ('poll_deadline', models.DateField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='PollVotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opt1', models.BooleanField(default=False)),
                ('opt2', models.BooleanField(default=False)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
