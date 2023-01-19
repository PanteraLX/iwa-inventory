from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import InventoryItem
from django.views.generic import ListView, UpdateView, DetailView
from app.forms import InventoryItemForm
from django.contrib.auth.models import User, Group


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


active_inventory_items_list = InventoryItemListView.as_view(
    queryset=InventoryItem.objects.active()[:5],
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',
)

complete_inventory_items_list = InventoryItemListView.as_view(
    queryset=InventoryItem.objects.all(),
    context_object_name='inventory_items_list',
    template_name='inventory/inventory_items.html',    
)




# A detail view of a single InventoryItem instance


class InventoryItemDetailView(DetailView):
    model = InventoryItem
    template_name = 'inventory/inventory_item_detail.html'
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
                      'inventory/create_update_inventory_item.html',
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
                      'inventory/create_update_inventory_item.html',
                      {'form': form})

def home(request):
    return render(request, 'app/home.html')


def index(request):
    return render(request, 'app/index.html')


def about(request):
    return render(request, 'app/about.html')


def contact(request):
    return render(request, 'app/contact.html')

