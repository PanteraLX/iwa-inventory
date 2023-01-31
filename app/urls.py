from django.urls import path
from app.views.order import OrderDetailView, OrderListView, OrderFormView, order_pdf, orders_by_item
from app.views.account import AccountDetailView, AccountListView, AccountFormView, AccountRegisterFormView
from app.views.inventory_item import InventoryItemDetailView, InventoryItemFormView, ActiveInventoryItemHomeListView, InventoryItemListView, ActiveInventoryItemListView,InactiveInventoryItemListView, inventory_item_unarchive, inventory_item_archive
from app.views.category import CategoryDetailView, CategoryListView, CategoryFormView

urlpatterns = [
    path('', ActiveInventoryItemHomeListView.as_view(), name='inventory_items'),
    path('inventory_items', ActiveInventoryItemListView.as_view(), name='inventory_items'),
    path('inventory_item/<int:pk>/update', InventoryItemFormView.as_view(), name='inventory_item_update'),
    path('inventory_item/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory_item_detail'),
    path('inventory_item/create', InventoryItemFormView.as_view(), name='inventory_item_create'),
    path('inventory_item/archive/<int:pk>/', inventory_item_archive, name='archive_inventory_item'),
    path('inventory_item/unarchive/<int:pk>/', inventory_item_unarchive, name='unarchive_inventory_item'),
    path('inventory_item/complete', InventoryItemListView.as_view(), name='complete_inventory_items_list'),
    path('inventory_item/archive', InactiveInventoryItemListView.as_view(), name='archive_inventory_items_list'),
   

    path('account/<int:pk>/update', AccountFormView.as_view(), name='user_update'),
    path('account/<int:pk>/orders', OrderListView.as_view(), name='user_orders'),
    path('account/<int:pk>', AccountDetailView.as_view(), name='user_detail'),
    path('account/create', AccountFormView.as_view(), name='user_create'),
    path('account/register', AccountRegisterFormView.as_view(), name='user_register'),
    path('accounts', AccountListView.as_view(), name='user_list'),

    path('category/<int:pk>/update', CategoryFormView.as_view(), name='category_update'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('category/create', CategoryFormView.as_view(), name='category_create'),
    path('categories', CategoryListView.as_view(), name='category_list'),

    path('order/<int:pk>/update', OrderFormView.as_view(), name='order_update'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order_detail'),
    path('order/create', OrderFormView.as_view(), name='order_create'),
    path('orders', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/pdf', order_pdf, name='order_pdf'),

    path('api/orders-by-item/<int:pk>', orders_by_item, name='order_by_item'),
]