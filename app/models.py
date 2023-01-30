from django.db import models
from django.contrib.auth.models import User as DjangoUser
from hashlib import sha1
import random

class ActiveManager(models.Manager):
    def active(self):
        return self.model.objects.filter(active=True)
    def inactive(self):
        return self.model.objects.filter(active=False)

class InventoryItem(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Item Name',
        help_text='Name of the Item'
    )
    producer = models.CharField(
        max_length=200,
        verbose_name='Producer',
        help_text='Producer of them Items'
    )
    description = models.TextField(
        verbose_name='Description',
        help_text='Detailed desscription of the Item'
    )

    position = models.CharField(
        max_length=200,
        verbose_name='Position',
        help_text='Position in the basement'
    )

    active = models.BooleanField(
        default=True, 
        editable=False,
        verbose_name='Active',
        help_text='Item ist active'
    )

    objects = ActiveManager()

    def __str__(self):
        return self.name

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

# A model for single inventory items that with a foreign key to the InventoryItem model, contains all the attributes
# of the InventoryItem model, but also has a hash to uniquely identify the item and a field called 'serial_number'
# which is the serial number of the item.
def _createHash():
    """This function generates a 40 character long hash"""
    encoded_rand = str(random.getrandbits(64)).encode('utf-8')
    encoded_rand = sha1(encoded_rand).hexdigest()
    return  encoded_rand

class SingleInventoryItem(models.Model):
    inventory_item = models.ForeignKey(
        InventoryItem,
        default=None,
        on_delete=models.CASCADE,
        )
    hash = models.CharField(
        max_length=48,
        default=_createHash,
        unique=True,
        verbose_name='Hash',
        help_text='Hash of the Item'
    )
    serial_number = models.CharField(
        max_length=200,
        verbose_name='Serial Number',
        help_text='Serial Number of the Item'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text='Item ist active'
    )

    objects = ActiveManager()

    def __str__(self):
        return self.inventory_item.name + " " + self.serial_number

# A model for the lendings of the items
class Lend(models.Model):
    user = models.ForeignKey(
        DjangoUser,
        on_delete=models.CASCADE,
        verbose_name='User',
        help_text='User'
    )
    item = models.ManyToManyField(
        SingleInventoryItem,
        on_delete=models.CASCADE,
        verbose_name='Item',
        help_text='Item'
    )

    quantity = models.IntegerField(
        verbose_name='Quantity',
        help_text='Quantity'
    )
    started_at = models.DateTimeField(
        null=True,
        verbose_name='Start',
        help_text='Start of the Order'
    )
    ended_at = models.DateTimeField(
        null=True,
        verbose_name='End',
        help_text='End of the Order'
    )

    returned = models.BooleanField(
        default=False,
        verbose_name='Returned',
        help_text='Item was returned'
    )

    def __str__(self):
        return self.item.name + " ordered by " + self.user.username