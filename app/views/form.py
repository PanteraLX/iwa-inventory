from django.views.generic import View
from django.shortcuts import render, redirect
from app.views.view_mixin import ViewMixin


class CustomFormView(ViewMixin, View):
    ''' A custom form view that can be used to create and update objects'''
    template_name = None
    form_class = None
    model = None
    success_url = None
    context = {}

    def get(self, request, *args, **kwargs):
        ''' GET request handler'''
        pk = self.extract_pk(kwargs)
        form = self.form_class(instance=self.extract_object(pk))
        return render(request, self.template_name, {'form': form, **self.get_context_data(request, *args, **kwargs)})

    def post(self, request, *args, **kwargs):
        ''' POST request handler'''
        pk = self.extract_pk(kwargs)
        form = self.form_class(request.POST, request.FILES, instance=self.extract_object(pk))
        if form.is_valid():
            object = form.save(commit=False)
            object.save()
            return redirect(self.success_url, pk=object.id)
        return render(request, self.template_name, {'form': form, **self.get_context_data(request, *args, **kwargs)})

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {**self.context}