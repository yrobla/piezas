from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, FormView
from django.core.urlresolvers import reverse
from oscar.core.loading import get_model
import forms


class HomeView(FormView):
    form_class = forms.SearchCreationForm
    template_name = 'search/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.SearchCreationFormSet(self.request.POST)
        else:
            context['formset'] = forms.SearchCreationFormSet()
        return context
    
    def form_valid(self, form):
        response = super(HomeView, self).form_valid(form)

        messages.success(self.request, _('Piece has been successfully added to search request'),
                         extra_tags='safe noicon')

        return response

    def get_success_url(self):
        return reverse('search:home')
