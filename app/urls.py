from django.urls import path
from app import views
from app.views.account import *
from app.views.lend import *
from app.views.inventory_item import ActiveInventoryItemHomeListView, ActiveInventoryItemListView, InactiveInventoryItemListView, InventoryItemFormView, InventoryItemDetailView, InventoryItemListView, inventory_item_archive, inventory_item_unarchive
from app.views.category import CategoryDetailView, CategoryListView, CategoryFormView
from app.views.single_inventory_item import  SingleInventoryItemDetailView, SingleInventoryItemFormView, single_inventory_item_create, single_inventory_item_delete
urlpatterns = [
    path('', ActiveInventoryItemHomeListView.as_view(), name='inventory_items'),
    path('inventory_items', ActiveInventoryItemListView.as_view(), name='inventory_items'),
    path('inventory_item/<int:pk>/update', InventoryItemFormView.as_view(), name='inventory_item_update'),
    path('inventory_item/<int:pk>/', InventoryItemDetailView.as_view(), name='inventory_item_detail'),
    path('inventory_item/single/<slug:hash>', SingleInventoryItemDetailView.as_view(), name='single_inventory_item_detail'),
    path('inventory_item/<int:pk>/single_inventory_item_create', single_inventory_item_create, name='single_inventory_item_create'),
    path('inventory_item/single/<slug:hash>/update', SingleInventoryItemFormView.as_view(), name='single_inventory_item_update'),
    path('inventory_item/single/<slug:hash>/delete', single_inventory_item_delete, name='single_inventory_item_delete'),
    path('inventory_item/create', InventoryItemFormView.as_view(), name='inventory_item_create'),
    path('inventory_item/archive/<int:pk>/', inventory_item_archive, name='archive_inventory_item'),
    path('inventory_item/unarchive/<int:pk>/', inventory_item_unarchive, name='unarchive_inventory_item'),
    path('inventory_item/complete', InventoryItemListView.as_view(), name='complete_inventory_items_list'),
    path('inventory_item/archive', InactiveInventoryItemListView.as_view(), name='archive_inventory_items_list'),
   

    path('account/<int:pk>/update', AccountFormView.as_view(), name='user_update'),
    path('account/<int:pk>/lends', LendListView.as_view(), name='user_lends'),
    path('account/<int:pk>', AccountDetailView.as_view(), name='user_detail'),
    path('account/create', AccountFormView.as_view(), name='user_create'),
    path('account/register', AccountRegisterFormView.as_view(), name='user_register'),
    path('accounts', AccountListView.as_view(), name='user_list'),

    path('category/<int:pk>/update', CategoryFormView.as_view(), name='category_update'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('category/create', CategoryFormView.as_view(), name='category_create'),
    path('categories', CategoryListView.as_view(), name='category_list'),
    
    path('lend/<int:pk>/upload_signed_receipt', upload_signed_receipt, name='upload_signed_receipt'),
    path('lend/<int:pk>/update', LendUpdateView.as_view(), name='lend_update'),
    path('lend/<int:pk>/delete', lend_delete, name='lend_delete'),
    path('lend/<int:pk>', LendDetailView.as_view(), name='lend_detail'),
    path('lend/create', LendFormView.as_view(), name='lend_create'),
    path('lend/<int:pk>/pdf', lend_pdf, name='lend_pdf'),
    path('lends', LendListView.as_view(), name='lend_list'),

    path('api/lends-by-item/<int:pk>', lends_by_item, name='lend_by_item'),

]