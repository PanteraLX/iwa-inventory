from django.shortcuts import render, redirect
from app.models import InventoryItem, InventoryItemImage
from app.forms import InventoryItemForm, InventoryItemImageForm
from django.views.generic import ListView, DetailView

# Switching the 'active' variable of an InventoryItem instance to False

def inventory_item_archive(request, id):
    inventory_item = InventoryItem.objects.get(id=id)
    inventory_item.active = False
    inventory_item.save()
    return redirect('complete_inventory_items_list')

# Switching the 'active' variable of an InventoryItem instance to True


def inventory_item_unarchive(request, id):
    inventory_item = InventoryItem.objects.get(id=id)
    inventory_item.active = True
    inventory_item.save()
    return redirect('inventory_items')

# A list view of all the InventoryItems


class InventoryItemListView(ListView):
    model = InventoryItem
    template_name = 'app/inventory_item_list.html'
    context_object_name = 'inventory_items'


active_inventory_items_list = InventoryItemListView.as_view(
    queryset=InventoryItem.objects.active(),
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',
)

complete_inventory_items_list = InventoryItemListView.as_view(
    queryset=InventoryItem.objects.all(),
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',    
)