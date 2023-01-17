# Generated by Django 4.1.5 on 2023-01-17 08:26

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
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name des Items', max_length=200, verbose_name='Item Name')),
                ('producer', models.CharField(help_text='Hersteller des Items', max_length=200, verbose_name='Hersteller')),
                ('description', models.TextField(help_text='Längere Beschreibung des Items', verbose_name='Beschreibung')),
                ('quantity', models.IntegerField(help_text='Anzahl', verbose_name='Anzahl')),
                ('position', models.CharField(help_text='Position im Lager', max_length=200, verbose_name='Position')),
                ('active', models.BooleanField(default=True, editable=False, help_text='Item ist aktiv', verbose_name='Aktiv')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('ACTIVE', 'active'), ('ARCHIVED', 'archived'), ('RESERVED', 'reserved')], default='ACTIVE', help_text='status', max_length=200, verbose_name='Status')),
                ('quantity', models.IntegerField(help_text='Anzahl', verbose_name='Anzahl')),
                ('started_at', models.DateTimeField(help_text='Beginn der Ausleihe', null=True, verbose_name='Beginn')),
                ('ended_at', models.DateTimeField(help_text='Ende der Ausleihe', null=True, verbose_name='Ende')),
                ('item', models.ForeignKey(help_text='Item', on_delete=django.db.models.deletion.CASCADE, to='app.inventoryitem', verbose_name='Item')),
                ('user', models.ForeignKey(help_text='Benutzer', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
        ),
    ]
