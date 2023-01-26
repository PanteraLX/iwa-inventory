from django.contrib import admin
from app.models import InventoryItem, Order, Category

admin.site.register(InventoryItem)
admin.site.register(Order)
admin.site.register(Category)


