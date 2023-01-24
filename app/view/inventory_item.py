from django.views.generic import DetailView, ListView
from app.forms import InventoryItemForm, InventoryItemImageForm
from app.view.form import CustomFormView
from django.shortcuts import render, redirect
from app.models import InventoryItem, InventoryItemImage


class InventoryItemDetailView(DetailView):
    ''' A detail view for the inventory item model'''
    model = InventoryItem
    template_name = 'inventory/inventory_item_detail.html'
    context_object_name = 'inventory_item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = InventoryItemImage.objects.filter(inventory_item=self.object)
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
        existing_images = InventoryItemImage.objects.filter(inventory_item=self.extract_object(pk))
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
