from django.utils.translation import ugettext as _

from oscar.apps.order.abstract_models import *  # noqa

class Order(AbstractOrder):
    payment_method = models.CharField(_('Payment method'), max_length=255)
    bank_account = models.CharField(_('IBAN account for transfer payment method'), max_length=255, blank=True, null=True)
