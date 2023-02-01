from django.views.generic import DetailView
from app.forms import InventoryItemForm, InventoryItemImageForm, SingleInventoryItemForm
from app.view.form import CustomFormView
from django.shortcuts import render, redirect
from app.models import *


class InventoryItemDetailView(DetailView):
    ''' A detail view for the inventory item model'''
    model = InventoryItem
    template_name = 'inventory/inventory_item_detail.html'
    context_object_name = 'inventory_item'

    def get_context_data(self, **kwargs):
        single_items = SingleInventoryItem.objects.filter(inventory_item=self.object)
        context = super().get_context_data(**kwargs)
        context['single_inventory_items'] = single_items
        context['images'] = InventoryItemImage.objects.filter(inventory_item=self.object)
        context['item_quantity'] = single_items.count()
        return context


class InventoryItemFormView(CustomFormView):
    ''' A custom form view that can be used to create and update inventory item objects'''
    template_name = 'inventory/inventory_item_update.html'
    form_class = InventoryItemForm
    model = InventoryItem
    success_url = 'inventory_item_detail'

    def get(self, request, *args, **kwargs):
        ''' GET request handler'''
        pk = self.extract_pk(kwargs)
        item = self.extract_object(pk)
        form = self.form_class(instance=item)
        new_images = InventoryItemImageForm()
        if pk:
            existing_images = InventoryItemImage.objects.filter(inventory_item=self.extract_object(pk))
            form.fields['quantity'].widget = form.fields['quantity'].hidden_widget()
        else:
            existing_images = None
        return render(request, self.template_name, 
                        {'form': form, 'new_images': new_images, 'existing_images': existing_images, 'item': item,
                        **self.get_context_data(request, *args, **kwargs)})

    def post(self, request, *args, **kwargs):
        ''' POST request handler'''
        pk = self.extract_pk(kwargs)
        form = self.form_class(request.POST, instance=self.extract_object(pk))
        image_form = InventoryItemImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if form.is_valid() and image_form.is_valid():

            # Save the inventory item and create the images
            inventory_item = form.save(commit=False)
            inventory_item.save()
            for image in images:
                InventoryItemImage.objects.create(inventory_item=inventory_item, image=image)

            # Create as many SingleInventoryItem objects as the 'quantity' field indicates when a new InventoryItem is created
            if not pk:
                for i in range(int(request.POST.get('quantity'))):
                    SingleInventoryItem.objects.create(inventory_item=inventory_item)

            # If the checkbox with name 'delete_image' is checked, delete the image with the id in value
            if 'delete_image' in request.POST:
                delete_image = request.POST.getlist('delete_image')
                for image in delete_image:
                    InventoryItemImage.objects.filter(id=image).delete()
    
            return redirect(self.success_url, pk=inventory_item.id)
        
        # If the form is not valid, render the form with the errors
        return render(request, self.template_name, {'form': form, 'image_form': image_form, **self.get_context_data(request, *args, **kwargs)})

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update',
                'new_existing_image': 'New Images' if self.extract_pk(kwargs) else 'Images',
                'existing_images_label': 'Existing Images' if self.extract_pk(kwargs) else '',
                }
    
# Detail view of the single inventory item model based on the hash in the url defined in urls.py
class SingleInventoryItemDetailView(DetailView):
    ''' A detail view for the single inventory item model'''
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