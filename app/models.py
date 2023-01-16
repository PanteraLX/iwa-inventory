from django.db import models

# Create your models here.


class InventoryItem(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Item Name',
        help_text='Name des Items'
    )
    producer = models.CharField(
        max_length=200,
        verbose_name='Hersteller',
        help_text='Hersteller des Items'
    )
    description = models.TextField(
        verbose_name='Beschreibung',
        help_text='Längere Beschreibung des Items'
    )
    quantity = models.IntegerField(
        verbose_name='Anzahl',
        help_text='Anzahl'
    )
    position = models.CharField(
        max_length=200,
        verbose_name='Position',
        help_text='Position im Lager'
    )

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Name',
        help_text='Name des Benutzers'
    )
    sur_name = models.CharField(
        max_length=200,
        verbose_name='Nachname',
        help_text='Nachname des Benutzers'
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Email-Adresse des Benutzers'
    )
    phone_number = models.CharField(
        max_length=200,
        verbose_name='Telefonnummer',
        help_text='Telefonnummer'
    )
    password = models.CharField(
        max_length=200,
        verbose_name='Passwort',
        help_text='Passwort'
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Benutzer',
        help_text='Benutzer'
    )
    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        verbose_name='Item',
        help_text='Item'
    )
    state = models.CharField(
        max_length=200,
        verbose_name='Status',
        help_text='status'
    )
    quantity = models.IntegerField(
        verbose_name='Anzahl',
        help_text='Anzahl'
    )
    started_at = models.DateTimeField(
        null=True,
        verbose_name='Beginn',
        help_text='Beginn der Ausleihe'
    )
    ended_at = models.DateTimeField(
        null=True,
        verbose_name='Ende',
        help_text='Ende der Ausleihe'
    )

    def __str__(self):
        return self.item.name + " ordered by " + self.user.name
