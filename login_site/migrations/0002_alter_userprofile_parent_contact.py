# Generated by Django 4.2.3 on 2023-08-12 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_site', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='parent_contact',
            field=models.IntegerField(null=True),
        ),
    ]
