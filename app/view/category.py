
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from app.forms import CategoryForm
from app.models import Category
from app.view.form import CustomFormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect


class CategoryDetailView(DetailView):
    ''' A detail view for the category model'''
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'


class CategoryListView(ListView):
    ''' A list view for the category models'''
    model = Category
    queryset = Category.objects.all()
    template_name = 'category/category_list.html'
    context_object_name = 'categories'


class CategoryFormView(CustomFormView):
    ''' A custom form view that can be used to create and update category objects'''
    template_name = 'category/category_update.html'
    form_class = CategoryForm
    model = Category
    success_url = 'category_detail'

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update'}
