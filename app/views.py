from django.shortcuts import render, redirect
from app.models import InventoryItem, Order
from django.views.generic import ListView





# Switching the 'active' variable of an InventoryItem instance to False


def inventory_item_archive(request, pk):
    inventory_item = InventoryItem.objects.get(id=pk)
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


active_inventory_items_list_home = InventoryItemListView.as_view(
    queryset=InventoryItem.objects.active()[:8],
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',
)

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

archive_inventory_items_list = InventoryItemListView.as_view(
    queryset=InventoryItem.objects.inactive(),
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',
)

# Pagination
class ActiveInventoryItemListViewPaginated(ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_items.html'
    context_object_name = 'inventory_items'
    paginate_by = 4

active_inventory_items_list_paginated = ActiveInventoryItemListViewPaginated.as_view(
    queryset=InventoryItem.objects.active(),
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',
)

class CompleteInventoryItemListViewPaginated(ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_items.html'
    context_object_name = 'inventory_items'
    paginate_by = 12

complete_inventory_items_list_paginated = CompleteInventoryItemListViewPaginated.as_view(
    queryset=InventoryItem.objects.all(),
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',
)

class ArchiveInventoryItemListViewPaginated(ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_items.html'
    context_object_name = 'inventory_items'
    paginate_by = 12

archive_inventory_items_list_paginated = ArchiveInventoryItemListViewPaginated.as_view(
    queryset=InventoryItem.objects.inactive(),
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',
)