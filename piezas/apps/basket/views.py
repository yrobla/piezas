from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from oscar.core.loading import get_class
	
PlaceSearchRequestForm = get_class('basket.forms', 'PlaceSearchRequestForm')

class PlaceSearchRequestView(FormView):
    template_name = 'basket/placesearchrequest.html'
    form_class = PlaceSearchRequestForm
    success_url = reverse_lazy('basket:placed-ok')

    def get_context_data(self, **kwargs):
        context = super(PlaceSearchRequestView, self).get_context_data(**kwargs)
        context['basket'] = self.request.basket
        return context
