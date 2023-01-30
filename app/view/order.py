from django.views.generic import DetailView, ListView
from app.forms import OrderForm
from app.view.form import CustomFormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from app.models import Order
from django.utils import timezone
from django.http import JsonResponse
from django.core.serializers import serialize
import json
import io
from django.http import HttpResponse, FileResponse
from fpdf import FPDF


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
        ''' Returns the context data for the view '''
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            orders = orders.filter(user=self.request.user)
        current_orders = {'data': orders.filter(ended_at__gte=timezone.now(), returned=False), 'title': 'Current Orders'}
        past_due_orders = {'data': orders.filter(ended_at__lt=timezone.now(), returned=False), 'title': 'Past Due Orders'}
        settled_orders = {'data': orders.filter(returned=True), 'title': 'Settled Orders'}
        context['all'] = [current_orders, past_due_orders, settled_orders]
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


def orders_by_item(request, pk):
    orders = Order.objects.filter(item=pk, returned=False)
    serialized_data = serialize("json", orders)
    serialized_data = json.loads(serialized_data)
    return JsonResponse(serialized_data, safe=False, status=200)


def order_pdf(request, pk):
    order = Order.objects.get(id=pk)
    file_name = f'order_{order.id}.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    content = io.BytesIO(bytes(pdf.output(dest = 'S'), encoding='latin1'))
    return FileResponse(content, content_type='application/pdf', as_attachment=True, filename=file_name)
