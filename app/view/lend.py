from django.views.generic import DetailView, ListView
from app.forms import LendForm
from app.view.form import CustomFormView
from app.models import Lend
from django.utils import timezone


class LendDetailView(DetailView):
    ''' A detail view for the lend model'''
    model = Lend
    template_name = 'lend/lend_detail.html'
    context_object_name = 'lend'

class LendListView(ListView):
    ''' A list view for the lend model'''
    model = Lend
    template_name = 'lend/lend_list.html'
    context_object_name = 'lends'
    
    # Get all lends
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lends = Lend.objects.all()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            lends = lends.filter(user=self.request.user)
        current_lends = lends.filter(ended_at__gte=timezone.now(), returned=False)
        past_due_lends = lends.filter(ended_at__lt=timezone.now(), returned=False)
        settled_lends = lends.filter(returned=True)
        context['all'] = current_lends
        context['past_due'] = past_due_lends
        context['settled'] = settled_lends
        return context
    
class LendFormView(CustomFormView):
    ''' A custom form view that can be used to create and update lend objects'''
    template_name = 'lend/lend_update.html'
    form_class = LendForm
    model = Lend
    success_url = 'lend_detail'

    # If a lend is created, associate it with as many SingleInventoryItem objects as the 'quantity' field indicates
    def get(self, request, *)

    def get_context_data(self, request, *args, **kwargs):
        ''' Returns the context data for the view'''
        return {'method': 'Create' if not self.extract_pk(kwargs) else 'Update', 'pk': self.extract_pk(kwargs)}
