from django import forms
from app.models import InventoryItem, SingleInventoryItem, InventoryItemImage, Lend, Category
from django.forms import ClearableFileInput
from django.contrib.auth.models import User as DjangoUser

class InventoryItemForm(forms.ModelForm):
    '''Form for creating and editing InventoryItems'''
    class Meta:
        ''' Meta class for InventoryItemForm'''
        model = InventoryItem
        fields = ['name', 'category', 'description', 'priceperunit', 'position', 'producer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'iwa-input w-full'}),
            'category': forms.Select(attrs={'class': 'iwa-input w-full'}),
            'priceperunit': forms.NumberInput(attrs={'class': 'iwa-input w-full', 'step':'1.0'}),
            'description': forms.Textarea(attrs={'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500'}),
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
    
class SingleInventoryItemForm(forms.ModelForm):
    '''Form for creating and editing SingleInventoryItems'''
    class Meta:
        '''Meta class for SingleInventoryItemForm'''
        model = SingleInventoryItem
        fields = ['inventory_item', 'serial_number', 'active']
        widgets = {
            'inventory_item': forms.Select(attrs={'class': 'iwa-input'}),
            'serial_number': forms.TextInput(attrs={'class': 'iwa-input'}),
            'active': forms.CheckboxInput(attrs={'class': 'iwa-input w-1/2', 'style': 'width: 1.5rem;'}),
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

lend_css_class = 'iwa-input w-full'
class LendForm(forms.ModelForm):
    '''Form for creating and editing Orders'''
    # The item field shows a selection of all inventory items
    item = forms.ModelChoiceField(queryset=InventoryItem.objects.all(), widget=forms.Select(attrs={'class': lend_css_class}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': lend_css_class}))

    class Meta:
        '''Meta class for LendForm'''
        model = Lend
        fields = ['item', 'user', 'returned', 'started_at', 'ended_at', 'document']
        widgets = {
            'user': forms.Select(attrs={'class': lend_css_class}),
            'item': forms.Select(attrs={'class': lend_css_class}),
            'returned': forms.CheckboxInput(attrs={'class': f'{lend_css_class} w-1/2', 'style': 'width: 1.5rem;'}),
            'started_at': forms.DateInput(attrs={'class': lend_css_class, 'type': 'date'}, format='%Y-%m-%d'),
            'ended_at': forms.DateInput(attrs={'class': lend_css_class, 'type': 'date'}, format='%Y-%m-%d'),
            'document': forms.FileInput(attrs={'type': 'file'}),
        }
    def __init__(self, *args, **kwargs):
        '''Initialize the LendForm'''
        super().__init__(*args, **kwargs)
        try:
            kwargs['instance']
            # Disable the 'returned' field if the order has not been created yet or the user is not an admin
            if kwargs['instance'] is None or not kwargs['instance'].user.is_superuser:
                # Hide de 'returned' field along with its label
                self.fields['returned'].label = ''
                self.fields['returned'].widget = forms.HiddenInput()
            if kwargs['instance'] is not None:
                # Show the name of the inventory_item associated with the first single inventory item associated 
                # with the lend in the item field and disable it.
                self.fields['item'].initial = kwargs['instance'].single_item.first().inventory_item
                self.fields['item'].required = False
                self.fields['item'].widget.attrs['disabled'] = True
                # Show the name of the user associated with the lend in the user field and disable it.
                self.fields['user'].initial = kwargs['instance'].user
                self.fields['user'].required = False
                self.fields['user'].widget.attrs['disabled'] = True
                # Show the number of single inventory items associated with the lend in the quantity field and disable it.
                self.fields['quantity'].initial = kwargs['instance'].single_item.count()
                self.fields['quantity'].required = False
                self.fields['quantity'].widget.attrs['disabled'] = True

            if kwargs['instance'] is None or kwargs['instance'].document:
                self.fields['document'].widget = forms.HiddenInput()
                self.fields['document'].label = ''
        except:
            pass
            

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

