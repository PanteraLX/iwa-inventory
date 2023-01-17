from django.urls import path
from app import views
from app.models import InventoryItem

inventory_items_list = views.InventoryItemListView.as_view(
    queryset=InventoryItem.objects.all()[:5],
    context_object_name='inventory_items_list',
    template_name='app/home.html',
)

urlpatterns = [
    path('', inventory_items_list, name='home'),
    path('create_inventory_item/', views.create_inventory_item, name='create_inventory_item'),
    path('archive/<int:id>/', views.inventory_item_archive, name='archive_inventory_item'),
]

