from django.views.generic import DetailView, ListView
from app.forms import InventoryItemForm
from app.view.form import CustomFormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from app.models import InventoryItem


class InventoryItemDetailView(DetailView):
    ''' A detail view for the inventory item model'''
    model = InventoryItem
    template_name = 'inventory/inventory_item_detail.html'
    context_object_name = 'inventory_item'


class InventoryItemFormView(CustomFormView):
    ''' A custom form view that can be used to create and update inventory item objects'''
    template_name = 'inventory/inventory_item_update.html'
    form_class = InventoryItemForm
    model = InventoryItem
    success_url = 'inventory_item_detail'

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update'}
