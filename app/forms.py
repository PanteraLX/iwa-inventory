from django import forms
from app.models import InventoryItem, InventoryItemImage
from django.forms import ClearableFileInput


inventory_item_css_class = 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'

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
        



