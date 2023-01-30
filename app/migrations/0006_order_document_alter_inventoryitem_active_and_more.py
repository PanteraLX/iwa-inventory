# Generated by Django 4.1.5 on 2023-01-26 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_remove_order_state_order_returned_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='document',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
    ]
