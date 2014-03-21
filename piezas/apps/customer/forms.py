from django.db import models
from django.utils.translation import ugettext_lazy as _

from oscar.core.compat import get_user_model
from oscar.apps.customer.forms import EmailUserCreationForm
from piezas.models import TYPE_CHOICES

User = get_user_model()

class PodEmailUserCreationForm(EmailUserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'type', 'cif', 'promotional_code')

    type = models.CharField(_('Customer type'), choices=TYPE_CHOICES, default='customer')
    cif = models.CharField(_('CIF'), max_length=9)
    promotional_code = models.CharField(_('Promotional code'), max_length=50)
