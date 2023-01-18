from django.urls import path
from app import views
from app.models import InventoryItem

urlpatterns = [
    path('', views.active_inventory_items_list, name='inventory_items'),
    path('inventory_item/<int:pk>/update',views.UpdateView, name='inventory_item_update'),
    path('inventory_item/<int:pk>/',views.InventoryItemDetailView.as_view(), name='inventory_item_detail'),
    path('inventory_item/create',views.create_inventory_item, name='inventory_item_create'),
    path('inventory_item/archive/<int:id>/', views.inventory_item_archive, name='archive_inventory_item'),
    path('inventory_item/unarchive/<int:id>/', views.inventory_item_unarchive, name='unarchive_inventory_item'),
    path('inventory_item/complete', views.complete_inventory_items_list, name='complete_inventory_items_list'),
    path('account/<int:pk>/update', views.create_user, name='user_update'),
    path('account/<int:pk>', views.UserItemDetailView.as_view(), name='user_detail'),
    path('account/create', views.create_user, name='user_create'),
]