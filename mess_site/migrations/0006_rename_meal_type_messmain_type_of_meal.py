# Generated by Django 4.1.2 on 2022-12-29 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mess_site', '0005_remove_extrasorder_username_extrasorder_item_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messmain',
            old_name='meal_type',
            new_name='type_of_meal',
        ),
    ]
