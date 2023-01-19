from django import forms
from app.models import InventoryItem, InventoryItemImage, Order
from django.forms import ClearableFileInput
from django.contrib.auth.models import User as DjangoUser

inventory_item_css_class = 'iwa-input'

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'description', 'quantity', 'position', 'producer']
        widgets = {
            'name': forms.TextInput(attrs={'class': inventory_item_css_class}),
            'description': forms.Textarea(attrs={'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500'}),
            'quantity': forms.NumberInput(attrs={'class': inventory_item_css_class}),
            'position': forms.TextInput(attrs={'class': inventory_item_css_class}),
            'producer': forms.TextInput(attrs={'class': inventory_item_css_class}),
        }

class InventoryItemImageForm(forms.ModelForm):
    class Meta:
        model = InventoryItemImage
        fields = ['image']
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }
        

user_css_class = 'iwa-input'

class AccountForm(forms.ModelForm):
    class Meta:
        model = DjangoUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': user_css_class}),
            'first_name': forms.TextInput(attrs={'class': user_css_class}),
            'last_name': forms.TextInput(attrs={'class': user_css_class}),
            'email': forms.TextInput(attrs={'class': user_css_class}),
        }


order_css_class = 'iwa-input'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'item', 'state', 'quantity', 'started_at', 'ended_at']
        widgets = {
            'user': forms.Select(attrs={'class': order_css_class}),
            'item': forms.Select(attrs={'class': order_css_class}),
            'state': forms.Select(attrs={'class': order_css_class}),
            'quantity': forms.NumberInput(attrs={'class': order_css_class}),
            'started_at': forms.DateInput(attrs={'class': order_css_class, 'type': 'date'}, format='%Y-%m-%d'),
            'ended_at': forms.DateInput(attrs={'class': order_css_class, 'type': 'date'}, format='%Y-%m-%d'),
        }
