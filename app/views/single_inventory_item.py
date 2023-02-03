from django.views.generic import DetailView, ListView
from app.forms import SingleInventoryItemForm, InventoryItemImageForm
from app.views.form import CustomFormView
from app.views.view_mixin import ViewMixin
from django.shortcuts import render, redirect
from app.models import InventoryItem, SingleInventoryItem
from django.core.exceptions import PermissionDenied


# Detail view of the single inventory item model based on the hash in the url defined in urls.py
class SingleInventoryItemDetailView(DetailView):
    ''' A detail view for the single inventory item model'''


    def dispatch(self, request, *args, **kwargs):
        ''' Dispatches the request to the appropriate handler'''
        # Only authenticated users can view SignleInventoryItemDetailViews
        if request.user.is_superuser:
            return super(SingleInventoryItemDetailView, self).dispatch(request, *args, **kwargs)

        # If the user is not authenticated, raise a permission denied error
        raise PermissionDenied

    def get_object(self, queryset=None):
        return SingleInventoryItem.objects.get(hash=self.kwargs.get('hash'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_item'] = InventoryItem.objects.get(id=self.object.inventory_item.id)
        return context

    context_object_name = 'single_inventory_item'
    template_name = 'inventory/single_inventory_item_detail.html'


# Update view of the single inventory item model
class SingleInventoryItemFormView(CustomFormView):
    template_name = 'inventory/single_inventory_item_update.html'
    form_class = SingleInventoryItemForm
    model = SingleInventoryItem
    success_url = 'single_inventory_item_detail'

    def dispatch(self, request, *args, **kwargs):
        ''' Dispatches the request to the appropriate handler'''
        # Only authenticated users can view SingleInventoryItemFormView
        if request.user.is_superuser:
            return super(SingleInventoryItemFormView, self).dispatch(request, *args, **kwargs)

        # If the user is not authenticated, raise a permission denied error
        raise PermissionDenied


    def get(self, request, *args, **kwargs):
        ''' GET request handler'''
        item = SingleInventoryItem.objects.get(hash=self.kwargs.get('hash'))
        form = self.form_class(instance=item)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        ''' POST request handler'''
        form = self.form_class(request.POST, instance=SingleInventoryItem.objects.get(hash=self.kwargs.get('hash')))
        if form.is_valid():
            form.save()
            return redirect(self.success_url, hash=self.kwargs.get('hash'))


# Delete a single inventory item with a function view
def single_inventory_item_delete(request, hash):
    ''' Deletes a single inventory item'''
    single_item = SingleInventoryItem.objects.get(hash=hash)
    single_item.delete()
    return redirect('inventory_item_detail', pk=InventoryItem.objects.get(id=single_item.inventory_item.id).id)


# Create a new single inventory item with a function view
def single_inventory_item_create(request, pk):
    ''' Creates a new single inventory item'''
    inventory_item = InventoryItem.objects.get(id=pk)
    SingleInventoryItem.objects.create(inventory_item=inventory_item)
    return redirect('inventory_item_detail', pk=inventory_item.id)