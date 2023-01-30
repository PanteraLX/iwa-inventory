from django.contrib import admin
from app.models import InventoryItem, Lend, SingleInventoryItem, InventoryItemImage

# In the Admin UI create a filter for the lend model to only show lends that have not yet been returned
class LendAdmin(admin.ModelAdmin):
    list_filter = ('returned',)
    list_display = ('item', 'returned')

admin.site.register(InventoryItem)
admin.site.register(Lend, LendAdmin)
admin.site.register(SingleInventoryItem)
admin.site.register(InventoryItemImage)


