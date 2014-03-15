from django.db import models
from django.utils.translation import ugettext as _
from oscar.core.compat import AUTH_USER_MODEL
from piezas import settings
import managers
from abstract_models import AbstractBasket, AbstractLine

class Basket(AbstractBasket):
    pass


class Line(AbstractLine):
    pass
