# Generated by Django 4.1.2 on 2023-03-01 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('query', '0005_query_votes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField(default=True)),
                ('query', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='query.query')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]