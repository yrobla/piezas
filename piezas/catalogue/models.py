from django.db import models
from django.utils.translation import ugettext as _
from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.apps.catalogue.models import ProductImage


class Brand(models.Model):
    name = models.CharField(_('Car brand'), max_length=255)

class Model(models.Model):
    brand = models.ForeignKey(Brand, verbose_name = _('Car brand'))
    name = models.CharField(_('Car model'), max_length=255)

class Version(models.Model):
    model = models.ForeignKey(Model, verbose_name = _('Car model'))
    name = models.CharField(_('Car model'), max_length=255)

class Bodywork(models.Model):
    name = models.CharField(_('Car bodywork type'), max_length=255)

class Engine(models.Model):
    name = models.CharField(_('Car engine'), max_length=255)

class Product(AbstractProduct):
    brand = models.ForeignKey(Brand, verbose_name=_("Car brand"),
        help_text=_('Brand of the car that it belongs to'), blank=True, null=True,
        related_name='product_brand')
    model = models.ForeignKey(Brand, verbose_name=_("Car model"),
        help_text=_('Model of the car that it belongs to'), blank=True, null=True,
        related_name='product_model')
    version = models.ForeignKey(Version, verbose_name=_("Car version"),
        help_text=_('Version of the car that it belongs to'), blank=True, null=True,
        related_name='product_version')
    bodywork = models.ForeignKey(Bodywork, verbose_name=_("Bodywork type"),
        blank=True, null=True, related_name='product_bodywork')
    engine = models.ForeignKey(Engine, verbose_name=_("Car engine"),
        blank=True, null=True, related_name='product_engine')
    frameref = models.CharField(_('Frame reference'), max_length=255, blank=True, null=True)

from oscar.apps.catalogue.models import *