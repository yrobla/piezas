from django import forms
from django.db.models import get_model
from oscar.apps.address.forms import AbstractAddressForm
from oscar.views.generic import PhoneNumberMixin
from piezas.apps.address.models import UserAddress
from django.utils.translation import ugettext_lazy as _

class UserAddressForm(AbstractAddressForm):

    latitude = forms.DecimalField(label=_('Latitude'), max_digits=40)
    longitude = forms.DecimalField(label=_('Longitude'), max_digits=40)

    class Meta:
        model = UserAddress
        exclude = ('title', 'user', 'num_orders', 'hash', 'search_text',
                   'notes', 'first_name', 'last_name', 'phone_number')

    def __init__(self, user, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        self.instance.user = user
        self.fields['country'].initial = 'ES'

