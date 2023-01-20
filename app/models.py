from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Create your models here.

class ActiveManager(models.Manager):
    def active(self):
        return self.model.objects.filter(active=True)

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

    active = models.BooleanField(
        default=True, 
        editable=False,
        verbose_name='Aktiv',
        help_text='Item ist aktiv'
    )

    objects = ActiveManager()

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        DjangoUser,
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

    STATE_CHOICES = (
        ('ACTIVE', 'active'),
        ('ARCHIVED', 'archived'),
        ('RESERVED', 'reserved'),
    )

    state = models.CharField(
        max_length=200,
        choices=STATE_CHOICES,
        default='ACTIVE',
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
        return self.item.name + " ordered by " + self.user.username

# A model for images that will be associated with the InventoryItem model

class InventoryItemImage(models.Model):
    inventory_item = models.ForeignKey(
        InventoryItem,
        default=None,
        on_delete=models.CASCADE,
        )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
        )
    image = models.FileField(
        upload_to='images/',
        blank=True,
        )
    
    def __str__(self):
        return self.inventory_item.name + " image"
