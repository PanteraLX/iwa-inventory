from django.urls import path
from app import views
from app.models import InventoryItem

active_inventory_items_list = views.InventoryItemListView.as_view(
    queryset=InventoryItem.objects.active()[:5],
    context_object_name='inventory_items_list',
    template_name='app/home.html',
)

complete_inventory_items_list = views.InventoryItemListView.as_view(
    queryset=InventoryItem.objects.all(),
    context_object_name='inventory_items_list',
    template_name='app/home.html',
)

urlpatterns = [
    path('', active_inventory_items_list, name='home'),
    path('create_inventory_item/', views.create_inventory_item, name='create_inventory_item'),
    path('archive/<int:id>/', views.inventory_item_archive, name='archive_inventory_item'),
    path('unarchive/<int:id>/', views.inventory_item_unarchive, name='unarchive_inventory_item'),
    path('complete/', complete_inventory_items_list, name='complete_inventory_items_list'),
]

