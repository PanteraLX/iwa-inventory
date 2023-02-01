from django.views.generic import DetailView, ListView, UpdateView
from app.forms import LendForm
from app.view.form import CustomFormView
from app.models import Lend, SingleInventoryItem
from django.utils import timezone
from django.shortcuts import render, redirect
from collections import namedtuple
from django.contrib import messages

class LendDetailView(DetailView):
    ''' A detail view for the lend model'''
    model = Lend
    template_name = 'lend/lend_detail.html'
    context_object_name = 'lend'

class LendListView(ListView):
    ''' A list view for the lend model'''
    model = Lend
    template_name = 'lend/lend_list.html'
    context_object_name = 'lends'
    
    # Get all lends
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lends = Lend.objects.all()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            lends = lends.filter(user=self.request.user)
        current_lends = lends.filter(ended_at__gte=timezone.now(), returned=False)
        past_due_lends = lends.filter(ended_at__lt=timezone.now(), returned=False)
        settled_lends = lends.filter(returned=True)
        context['all'] = current_lends
        context['past_due'] = past_due_lends
        context['settled'] = settled_lends
        return context
    
class LendFormView(CustomFormView):
    ''' A custom form view that can be used to create and update lend objects'''
    template_name = 'lend/lend_update.html'
    form_class = LendForm
    model = Lend
    success_url = 'lend_detail'

    # Get an empty lend form
    def get(self, request, *args, **kwargs):
        ''' GET request handler'''
        form = self.form_class()
        return render(request, self.template_name, {'form': form, **self.get_context_data(request, *args, **kwargs)})
    
    # Save the lend object and associate the SingleInventoryItem(s) with it
    def post(self, request, *args, **kwargs):
        pk = self.extract_pk(kwargs)
        lend = self.extract_object(pk)
        form = self.form_class(request.POST, instance=lend)
        if form.is_valid():
            lend = form.save()
            lend.save()
            # Get the started_at and ended_at dates
            started_at = form.cleaned_data['started_at']
            ended_at = form.cleaned_data['ended_at']
            # For every item, check if the lends it is associated with start after the lend ends or end before the lend starts
            # If this is the case, associate the item with the lend
            counter = 0
            items = SingleInventoryItem.objects.filter(inventory_item=form.cleaned_data['item'])
            Range = namedtuple('Range', ['start', 'end'])
            for item in items:
                # Check if the item has any lends associated with it
                if not item.lend_set.all():
                    lend.single_item.add(item)
                    lend.save()
                    counter += 1
                else:
                    # If the item has lends associated with it, check if the lend period overlaps with any of the reserved periods
                    reserved_periods = []
                    for item_lend in item.lend_set.all():
                        # Add the period between started_at and ended_at to the reserved periods as datetime objects
                        reserved_periods.append(Range(start=item_lend.started_at, end=item_lend.ended_at))
                    # Check if the lend period overlaps with any of the reserved periods
                    if not any(r.start <= ended_at and started_at <= r.end for r in reserved_periods):
                        lend.single_item.add(item)
                        lend.save()
                        counter += 1
                if counter == form.cleaned_data['quantity']:
                    return redirect(self.success_url, pk=lend.pk)
            # Return to the lend form and throw an error if the quantity of items is not enough
            if counter < form.cleaned_data['quantity']:
                lend.delete()
                messages.error(request, 'All items are already reserved for this period. Try another period or another item.')
                return redirect('lend_create')

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        context = super().get_context_data(request, *args, **kwargs)
        context['method'] = 'Create'
        return context
    
class LendUpdateView(UpdateView):
    ''' An update view for the lend model'''
    model = Lend
    template_name = 'lend/lend_update.html'
    form_class = LendForm
    success_url = 'lend_detail'

    def get(self, request, *args, **kwargs):
        ''' GET request handler'''
        pk = self.extract_pk(kwargs)
        lend = self.extract_object(pk)
        form = self.form_class(instance=lend)
        return render(request, self.template_name, {'form': form, 'lend': lend, **self.get_context_data(request, *args, **kwargs)})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['method'] = 'Update'
        return context

# Delete a given lend
def lend_delete(request, pk):
    ''' Delete a lend'''
    lend = Lend.objects.get(pk=pk)
    lend.delete()
    return redirect('lend_list')
