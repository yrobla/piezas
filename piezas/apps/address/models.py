from django.db import models
from django.utils.translation import ugettext_lazy as _

from oscar.apps.address.abstract_models import (
    AbstractUserAddress, AbstractCountry)

class UserAddress(AbstractUserAddress):
    latitude = models.DecimalField(_('Latitude'), max_digits=40, decimal_places=20)
    longitude = models.DecimalField(_('Longitude'), max_digits=40, decimal_places=20)

class Country(AbstractCountry):
    pass
