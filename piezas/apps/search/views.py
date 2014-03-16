from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from oscar.core.loading import get_model
import forms

class HomeView(CreateView):
    form_class = forms.SearchCreationForm
    template_name = 'search/home.html'
    model = get_model('catalogue', 'SearchProductRequest')
    
    def form_valid(self, form):
        response = super(HomeView, self).form_valid(form)

        # add that to basket
        basket = self.request.basket
        basket.add_product(form.instance, 1, None)

        messages.success(self.request, _('Piece has been successfully added to search request'),
                         extra_tags='safe noicon')

        return response

    def get_success_url(self):
        return reverse('search:home')
