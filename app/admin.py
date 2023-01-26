from django.contrib import admin
from app.models import InventoryItem, Order, SingleInventoryItem, InventoryItemImage

# In the Admin UI create a filter for the order model to only show orders that have not yet been returned
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('returned',)
    list_display = ('item', 'returned')

admin.site.register(InventoryItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(SingleInventoryItem)
admin.site.register(InventoryItemImage)


