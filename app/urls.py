from django.urls import path
from app import views
from app.view.account import AccountDetailView, AccountListView, AccountFormView
from app.view.order import OrderDetailView, OrderListView, OrderFormView
from app.view.inventory_item import InventoryItemDetailView, InventoryItemFormView


urlpatterns = [
    path('', views.active_inventory_items_list, name='inventory_items'),
    path('inventory_item/<int:pk>/update', InventoryItemFormView.as_view(), name='inventory_item_update'),
    path('inventory_item/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory_item_detail'),
    path('inventory_item/create', InventoryItemFormView.as_view(), name='inventory_item_create'),
    path('inventory_item/archive/<int:id>/', views.inventory_item_archive, name='archive_inventory_item'),
    path('inventory_item/unarchive/<int:id>/', views.inventory_item_unarchive, name='unarchive_inventory_item'),
    path('inventory_item/complete', views.complete_inventory_items_list, name='complete_inventory_items_list'),

    path('account/<int:pk>/update', AccountFormView.as_view(), name='user_update'),
    path('account/<int:pk>/orders', OrderListView.as_view(), name='user_orders'),
    path('account/<int:pk>', AccountDetailView.as_view(), name='user_detail'),
    path('account/create', AccountFormView.as_view(), name='user_create'),
    path('accounts', AccountListView.as_view(), name='user_list'),

    path('order/<int:pk>/update', OrderFormView.as_view(), name='order_update'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order/create', OrderFormView.as_view(), name='order_create'),
    path('orders', OrderListView.as_view(), name='order_list'),
]