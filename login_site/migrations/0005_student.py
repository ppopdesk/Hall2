# Generated by Django 4.1.2 on 2023-02-12 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_site', '0004_remove_user_otp_user_user_otp_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('roll_number', models.IntegerField()),
            ],
        ),
    ]