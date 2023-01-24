from django.views.generic import DetailView, ListView
from app.forms import OrderForm
from app.view.form import CustomFormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from app.models import Order
from django.utils import timezone


class OrderDetailView(DetailView):
    ''' A detail view for the order model'''
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

class OrderListView(ListView):
    ''' A list view for the order model'''
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    
    # Get all orders
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            orders = orders.filter(user=self.request.user)
        current_orders = orders.filter(ended_at__gte=timezone.now(), returned=False)
        past_due_orders = orders.filter(ended_at__lt=timezone.now(), returned=False)
        settled_orders = orders.filter(returned=True)
        context['all'] = current_orders
        context['past_due'] = past_due_orders
        context['settled'] = settled_orders
        return context
    
class OrderFormView(CustomFormView):
    ''' A custom form view that can be used to create and update order objects'''
    template_name = 'order/order_update.html'
    form_class = OrderForm
    model = Order
    success_url = 'order_detail'

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update', 'pk': self.extract_pk(kwargs)}
