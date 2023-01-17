from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import InventoryItem
from django.views.generic import ListView
from app.forms import InventoryItemForm

# Switching the 'active' variable of an InventoryItem instance to False

def inventory_item_archive(request, id):
    inventory_item = InventoryItem.objects.get(id=id)
    inventory_item.active = False
    inventory_item.save()
    return redirect('home')

# Switching the 'active' variable of an InventoryItem instance to True

def inventory_item_unarchive(request, id):
    inventory_item = InventoryItem.objects.get(id=id)
    inventory_item.active = True
    inventory_item.save()
    return redirect('complete_inventory_items_list')

# A list view of all the InventoryItems

class InventoryItemListView(ListView):
    model = InventoryItem
    template_name = 'app/inventory_item_list.html'
    context_object_name = 'inventory_items'

# A function-based view to create a new InventoryItem

def create_inventory_item(request):
    form = InventoryItemForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.save()
            return redirect('create_inventory_item')
    else:
        return render(request,
                        'app/create_inventory_item.html',
                        {'form': form})
