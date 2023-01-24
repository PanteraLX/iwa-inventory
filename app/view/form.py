from django.views.generic import View
from django.shortcuts import render, redirect


class CustomFormView(View):
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
        form = self.form_class(request.POST, instance=self.extract_object(pk))
        if form.is_valid():
            object = form.save(commit=False)
            object.save()
            return redirect(self.success_url, pk=object.id)
        return render(request, self.template_name, {'form': form, **self.get_context_data(request, *args, **kwargs)})

    def extract_pk(self, kwargs):
        ''' Extracts the primary key from the kwargs dictionary'''
        if kwargs and kwargs['pk']:
            return kwargs['pk']
        return None

    def extract_object(self, pk):
        ''' Extracts the object from the model based on the primary key'''
        if pk:
            return self.model.objects.get(id=pk)
        return None
