from django import forms
from app.models import InventoryItem
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


user_css_class = 'iwa-input'

class UserForm(forms.ModelForm):
    class Meta:
        model = DjangoUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': user_css_class}),
            'first_name': forms.TextInput(attrs={'class': user_css_class}),
            'last_name': forms.TextInput(attrs={'class': user_css_class}),
            'email': forms.TextInput(attrs={'class': user_css_class}),
        }


