
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import get_user_model
from app.forms import AccountForm
from app.view.form import CustomFormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.http import Http404
from app.view.view_mixin import ViewMixin


class AccountDetailView(ViewMixin, DetailView):
    ''' A detail view for the account model'''
    model = DjangoUser
    template_name = 'account/user_detail.html'
    context_object_name = 'user'

    def dispatch(self, request, *args, **kwargs):
        ''' Dispatches the request to the appropriate handler'''
        pk = self.extract_pk(kwargs)
        try:
            user = self.extract_object(pk)
        except DjangoUser.DoesNotExist:
            raise Http404
    
        logged_in_user = request.user

        # Only superusers can view other users. Users can only view their own account
        if logged_in_user.is_superuser or logged_in_user.id == user.id:
            return super(AccountDetailView, self).dispatch(request, *args, **kwargs)
        # If the user is not a superuser and is not viewing their own account, raise a permission denied error
        raise PermissionDenied



class AccountListView(ListView):
    ''' A list view for the account models'''
    model = DjangoUser
    queryset = DjangoUser.objects.all()
    template_name = 'account/user_list.html'
    context_object_name = 'users'

    def dispatch(self, request, *args, **kwargs):
        ''' Dispatches the request to the appropriate handler'''
        # Only superusers can view other users
        if request.user.is_superuser:
            return super(AccountDetailView, self).dispatch(request, *args, **kwargs)
        # If the user is not a superuser, raise a permission denied error
        raise PermissionDenied


class AccountFormView(CustomFormView):
    ''' A custom form view that can be used to create and update account objects'''
    template_name = 'account/user_update.html'
    form_class = AccountForm
    model = DjangoUser
    success_url = 'user_detail'

    def get(self, request, *args, **kwargs):
        ''' GET request handler'''
        pk = self.extract_pk(kwargs)
        user = self.extract_object(pk)
        logged_in_user = request.user

        # Only superusers can view other users. Users can only view their own account
        if not pk or logged_in_user.is_superuser or logged_in_user.id == user.id:
            form = self.form_class(instance=user)
            return render(request, self.template_name, {'form': form, **self.get_context_data(request, *args, **kwargs)})

        # If the user is not a superuser and is trying to view another user's account, raise a permission denied error
        raise PermissionDenied
            

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''

        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update'}
