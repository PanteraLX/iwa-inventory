from django.views.generic import DetailView, ListView
from app.forms import OrderForm
from app.view.form import CustomFormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from app.models import Order


class OrderDetailView(DetailView):
    ''' A detail view for the order model'''
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

class OrderListView(ListView):
    ''' A list view for the account models'''
    model = Order
    queryset = Order.objects.all()
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

class OrderFormView(CustomFormView):
    ''' A custom form view that can be used to create and update order objects'''
    template_name = 'order/order_update.html'
    form_class = OrderForm
    model = Order
    success_url = 'order_detail'

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update'}
