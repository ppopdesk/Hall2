# Generated by Django 4.1.2 on 2023-01-01 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_query_date_time_query_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Query',
        ),
    ]
