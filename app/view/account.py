
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import get_user_model
from app.forms import AccountForm
from app.view.form import CustomFormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect


class AccountDetailView(DetailView):
    ''' A detail view for the account model'''
    model = DjangoUser
    template_name = 'account/user_detail.html'
    context_object_name = 'user'


class AccountListView(ListView):
    ''' A list view for the account models'''
    model = DjangoUser
    queryset = DjangoUser.objects.all()
    template_name = 'account/user_list.html'
    context_object_name = 'users'


class AccountFormView(CustomFormView):
    ''' A custom form view that can be used to create and update account objects'''
    template_name = 'account/user_update.html'
    form_class = AccountForm
    model = DjangoUser
    success_url = 'user_detail'

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update'}
