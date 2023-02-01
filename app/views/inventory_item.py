from django.views.generic import DetailView, ListView
from app.forms import InventoryItemForm, InventoryItemImageForm
from app.views.form import CustomFormView
from app.views.view_mixin import ViewMixin
from app.views.single_inventory_item import SingleInventoryItem
from django.shortcuts import render, redirect
from app.models import InventoryItem, InventoryItemImage, Category
from django.core.exceptions import PermissionDenied

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

    def dispatch(self, request, *args, **kwargs):
        ''' Dispatches the request to the appropriate handler'''
        # Only authenticated users can view Itemforms
        if request.user .is_superuser:
            return super(InventoryItemFormView, self).dispatch(request, *args, **kwargs)

        # If the user is not authenticated, raise a permission denied error
        raise PermissionDenied

    def get(self, request, *args, **kwargs):
        ''' GET request handler'''
        pk = self.extract_pk(kwargs)
        item = self.extract_object(pk)
        form = self.form_class(instance=item)
        new_images = InventoryItemImageForm()
        if pk:
            existing_images = InventoryItemImage.objects.filter(inventory_item=self.extract_object(pk))
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
        return render(request, self.template_name,
                      {'form': form, 'image_form': image_form, **self.get_context_data(request, *args, **kwargs)})

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update',
                'new_existing_image': 'New Images' if self.extract_pk(kwargs) else 'Images',
                'existing_images_label': 'Existing Images' if self.extract_pk(kwargs) else '',
                'creation': not self.extract_pk(kwargs),
                }


class InventoryItemListView(ListView):
    ''' A list view for the inventory item model'''
    model = InventoryItem
    template_name = 'inventory/inventory_items.html'
    context_object_name = 'inventory_items_list'

class InventoryItemListViewPaginated(ViewMixin, InventoryItemListView):
    ''' A list view for the inventory item model (paginated)'''
    paginate_by = 4
    category = None
    search = None

    def setup(self, request, *args, **kwargs):
        ''' Sets up the view (is called before get_context_data)'''
        paginate_by = self.extract_query_value(request, 'paginate_by')
        if paginate_by and paginate_by != 'None':
            self.paginate_by = paginate_by

        category = self.extract_query_value(request, 'category')
        if category and category != 'None':
            self.queryset = self.queryset.filter(category=category)
            self.category = category

        search = self.extract_query_value(request, 'search')
        if search and search != 'None':
            self.queryset = self.queryset.filter(name__icontains=search)
            self.search = search
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ''' Returns the context data for the view '''
        context = super().get_context_data(**kwargs)
        context['paginate_by'] = self.paginate_by
        context['category'] = self.category
        context['search'] = self.search
        context['categories'] = Category.objects.all()
        return context


class ActiveInventoryItemHomeListView(InventoryItemListView):
    ''' A list view for the active inventory item model (home)'''
    queryset = InventoryItem.objects.active()[:8]

    def get_context_data(self, **kwargs):
        ''' Returns the context data for the view '''
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'home'
        return context

class ActiveInventoryItemListView(InventoryItemListViewPaginated):
    ''' A list view for the active inventory item model (paginated)'''
    queryset = InventoryItem.objects.active()

    def get_context_data(self, **kwargs):
        ''' Returns the context data for the view '''
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'active'
        return context

class InactiveInventoryItemListView(InventoryItemListViewPaginated):
    ''' A list view for the inactive inventory item model (paginated)'''
    queryset = InventoryItem.objects.inactive()

    def dispatch(self, request, *args, **kwargs):
        ''' Dispatches the request to the appropriate handler'''
        # Only authenticated users can view inactive Items
        if request.user .is_superuser:
            return super(InactiveInventoryItemListView, self).dispatch(request, *args, **kwargs)

        # If the user is not authenticated, raise a permission denied error
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        ''' Returns the context data for the view '''
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'inactive'
        return context


class InventoryItemListView(InventoryItemListViewPaginated):
    ''' A list view for the inventory item model (paginated)'''
    queryset = InventoryItem.objects.all()

    def get_context_data(self, **kwargs):
        ''' Returns the context data for the view '''
        context = super().get_context_data(**kwargs)
        context['page_name'] = 'complete'
        return context


def dispatch(self, request, *args, **kwargs):
    ''' Dispatches the request to the appropriate handler'''
    # Only authenticated users can view inactive Items
    if request.user .is_superuser:
        return super(InventoryItemListView, self).dispatch(request, *args, **kwargs)

    # If the user is not authenticated, raise a permission denied error
    raise PermissionDenied

# Switching the 'active' variable of an InventoryItem instance to False
def inventory_item_archive(request, pk):
    inventory_item = InventoryItem.objects.get(id=pk)
    inventory_item.active = False
    inventory_item.save()
    return redirect('complete_inventory_items_list')


# Switching the 'active' variable of an InventoryItem instance to True
def inventory_item_unarchive(request, id):
    inventory_item = InventoryItem.objects.get(id=id)
    inventory_item.active = True
    inventory_item.save()
    return redirect('inventory_items')