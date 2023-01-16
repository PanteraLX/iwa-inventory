from django.db import models

# Create your models here.

class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    quantity = models.IntegerField()
    position = models.CharField(max_length=200)
    producer = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=200)
    sur_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    state = models.CharField(max_length=200)

    def __str__(self):
        return self.item.name + " ordered by " + self.user.name
