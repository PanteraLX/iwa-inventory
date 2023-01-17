from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import InventoryItem
from django.views.generic import ListView, UpdateView, DetailView
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

# A detail view of a single InventoryItem instance

class InventoryItemDetailView(DetailView):
    model = InventoryItem
    template_name = 'app/inventory_item_detail.html'
    context_object_name = 'inventory_item'

# A function-based view to update an InventoryItem instance

def UpdateView(request, pk):
    inventory_item = InventoryItem.objects.get(id=pk)
    form = InventoryItemForm(request.POST or None, instance=inventory_item)

    if request.method == 'POST':
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.save()
            return redirect('inventory_item_detail', pk=inventory_item.pk)
    else:
        return render(request,
                        'app/inventory_item_update.html',
                        {'form': form})

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


def home(request):
    return render(request, 'inventory/home.html')

def index(request):
    return render(request, 'inventory/index.html')

def about(request):
    return render(request, 'inventory/about.html')

def contact(request):
    return render(request, 'inventory/contact.html')




