from django import forms
from django.conf import settings
from oscar.core.loading import get_model
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.utils.translation import ugettext_lazy as _

from oscar.forms import widgets

Line = get_model('basket', 'line')
Basket = get_model('basket', 'basket')
Product = get_model('catalogue', 'product')


class BasketLineForm(forms.ModelForm):
    save_for_later = forms.BooleanField(
        initial=False, required=False, label=_('Save for Later'))

    def __init__(self, strategy, *args, **kwargs):
        super(BasketLineForm, self).__init__(*args, **kwargs)
        self.instance.strategy = strategy

    def clean_quantity(self):
        qty = self.cleaned_data['quantity']
        if qty > 0:
            self.check_max_allowed_quantity(qty)
            self.check_permission(qty)
        return qty

    def check_max_allowed_quantity(self, qty):
        is_allowed, reason = self.instance.basket.is_quantity_allowed(qty)
        if not is_allowed:
            raise forms.ValidationError(reason)

    def check_permission(self, qty):
        return True

    class Meta:
        model = Line
        exclude = ('basket', 'product', 'stockrecord', 'line_reference',
                   'price_excl_tax', 'price_incl_tax', 'price_currency')


class PlaceSearchRequestForm(forms.Form):
    pass
