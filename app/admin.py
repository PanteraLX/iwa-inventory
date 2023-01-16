from django.contrib import admin
from app.models import User, InventoryItem, Order

admin.site.register(User)
admin.site.register(InventoryItem)
admin.site.register(Order)


