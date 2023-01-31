from django import forms
from app.models import InventoryItem, InventoryItemImage, Order, Category
from django.forms import ClearableFileInput
from django.contrib.auth.models import User as DjangoUser

class InventoryItemForm(forms.ModelForm):
    '''Form for creating and editing InventoryItems'''
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'description', 'quantity', 'position', 'producer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'category': forms.Select(attrs={'class': 'iwa-input w-full'}),
            'description': forms.Textarea(attrs={'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500'}),
            'quantity': forms.NumberInput(attrs={'class': 'iwa-input w-full'}),
            'position': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'producer': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
        }

class InventoryItemImageForm(forms.ModelForm):
    '''Form for creating and editing InventoryItemImages'''
    class Meta:
        '''Meta class for InventoryItemImageForm'''
        model = InventoryItemImage
        fields = ['image']
        widgets = {
            'image': ClearableFileInput(attrs={'multiple': True}),
        }
        


class AccountForm(forms.ModelForm):
    '''Form for creating and editing Accounts'''
    class Meta:
        '''Meta class for AccountForm'''
        model = DjangoUser
        fields = ['username', 'first_name', 'last_name', 'is_active', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'email': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
        }

class AccountRegisterForm(forms.ModelForm):
    '''Form for creating and editing Accounts'''
    class Meta:
        '''Meta class for AccountForm'''
        model = DjangoUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'first_name': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'email': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'password': forms.TextInput(attrs={'class': 'iwa-input w-full', 'type': 'password'}),
        }


order_css_class = 'iwa-input w-full'

class OrderForm(forms.ModelForm):
    '''Form for creating and editing Orders'''
    class Meta:
        '''Meta class for OrderForm'''
        model = Order
        fields = ['item', 'user', 'returned', 'quantity', 'started_at', 'ended_at', 'document']
        widgets = {
            'user': forms.Select(attrs={'class': order_css_class}),
            'item': forms.Select(attrs={'class': order_css_class}),
            'returned': forms.CheckboxInput(attrs={'class': f'{order_css_class} w-1/2', 'style': 'width: 1.5rem;'}),
            'quantity': forms.NumberInput(attrs={'class': order_css_class}),
            'started_at': forms.DateInput(attrs={'class': order_css_class, 'type': 'date'}, format='%Y-%m-%d'),
            'ended_at': forms.DateInput(attrs={'class': order_css_class, 'type': 'date'}, format='%Y-%m-%d'),
            'document': forms.FileInput(attrs={'type': 'file'}),
        }

    # Disable the 'returned' field if the order has not been created yet or the user is not an admin
    def __init__(self, *args, **kwargs):
        '''Initialize the OrderForm'''
        super().__init__(*args, **kwargs)
        if kwargs['instance'] is None or not kwargs['instance'].user.is_superuser:
            # Hide de 'returned' field along with its label
            self.fields['returned'].label = ''
            self.fields['returned'].widget = forms.HiddenInput()

        if kwargs['instance'] is None or kwargs['instance'].document:
            self.fields['document'].label = ''
            self.fields['document'].widget = forms.HiddenInput()


class CategoryForm(forms.ModelForm):
    '''Form for creating and editing Categories'''
    class Meta:
        '''Meta class for CategoryForm'''
        model = Category
        fields = ['name', 'description', 'color', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'description': forms.Textarea(attrs={'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500'}),
            'color': forms.TextInput(attrs={'class': 'iwa-input', 'type': 'color'}),
            'icon': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
        }