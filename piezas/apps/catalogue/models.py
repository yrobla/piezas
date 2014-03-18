from django.db import models
from django.utils.translation import ugettext as _
from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.apps.catalogue.models import ProductImage
from oscar.core.compat import AUTH_USER_MODEL
from smart_selects.db_fields import ChainedForeignKey
from oscar.apps.catalogue.models import Category

class BrandManager(models.Manager):

    def base_queryset(self):
        """
        Return ``QuerySet`` with related content pre-loaded.
        """
        return self.get_query_set().all()


class Brand(models.Model):
    name = models.CharField(_('Car brand'), max_length=255)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)
    objects = BrandManager()

    def __unicode__(self):
        return self.name


class ModelManager(models.Manager):

    def base_queryset(self):
        """
        Return ``QuerySet`` with related content pre-loaded.
        """
        return self.get_query_set().all()


class Model(models.Model):
    brand = models.ForeignKey(Brand, verbose_name = _('Car brand'))
    name = models.CharField(_('Car model'), max_length=255)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)
    objects = ModelManager()

    def __unicode__(self):
        return u'%s - %s' % (self.brand, self.name)


class VersionManager(models.Manager):

    def base_queryset(self):
        """
        Return ``QuerySet`` with related content pre-loaded.
        """
        return self.get_query_set().all()


class Version(models.Model):
    model = models.ForeignKey(Model, verbose_name = _('Car model'))
    name = models.CharField(_('Car version'), max_length=255)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)
    objects = VersionManager()

    def __unicode__(self):
        return u'%s - %s' % (self.model, self.name)


class BodyworkManager(models.Manager):

    def base_queryset(self):
        """
        Return ``QuerySet`` with related content pre-loaded.
        """
        return self.get_query_set().all()


class Bodywork(models.Model):
    name = models.CharField(_('Car bodywork type'), max_length=255)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)
    objects = BodyworkManager()

    def __unicode__(self):
        return self.name


class EngineManager(models.Manager):

    def base_queryset(self):
        """
        Return ``QuerySet`` with related content pre-loaded.
        """
        return self.get_query_set().all()


class Engine(models.Model):
    name = models.CharField(_('Car engine'), max_length=255)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)
    objects = EngineManager()

    def __unicode__(self):
        return self.name

class Product(AbstractProduct):
    pass


SEARCH_REQUEST_TYPES = (('regional', _('Regional')), ('border', _('Border area')),
    ('national', _('National')), ('supra', _('Supraregional')))

SEARCH_REQUEST_STATES = (('pending', _('Pending')), ('expired', _('Expired')),
    ('closed', _('Closed')))


class SearchRequest(models.Model):
    brand = models.ForeignKey(Brand, verbose_name=_("Brand"),
        blank=True, null=True, related_name='product_brand')
    model = ChainedForeignKey(Model, chained_field="brand", chained_model_field="brand",
        show_all=False, auto_choose=False, verbose_name=_("Car model"),
        help_text=_('Model of the car that it belongs to'), blank=True, null=True,
        related_name='product_model')
    version = ChainedForeignKey(Version, chained_field="model", chained_model_field="model",
        show_all=False, auto_choose=True, verbose_name=_("Car version"),
        help_text=_('Version of the car that it belongs to'), blank=True, null=True,
        related_name='product_version')
    bodywork = models.ForeignKey(Bodywork, verbose_name=_("Bodywork type"),
        blank=True, null=True, related_name='product_bodywork')
    engine = models.ForeignKey(Engine, verbose_name=_("Car engine"),
        blank=True, null=True, related_name='product_engine')
    frameref = models.CharField(_('Frame reference'), max_length=255, blank=True, null=True)
    comments = models.TextField(_('Comments'), blank=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)
    owner = models.ForeignKey(
        AUTH_USER_MODEL, related_name='search_requests', null=True,
        verbose_name=_("Owner"))
    search_type = models.CharField(max_length=25, choices=SEARCH_REQUEST_TYPES)
    state = models.CharField(max_length=25, choices=SEARCH_REQUEST_STATES, default='pending')
    expiration_date = models.DateTimeField(_('Expiration Date'), blank=True, null=True)


class SearchItemRequest(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Category'),
        help_text=_('Category to search for'), related_name='product_category')
    piece = ChainedForeignKey(Product, chained_field="category", chained_model_field="categories",
        show_all=False, auto_choose=False, verbose_name=_("Piece"),
        help_text=_('Piece to search for'), related_name='product_piece')
    comments = models.TextField(_('Comments'), blank=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    owner = models.ForeignKey(
        AUTH_USER_MODEL, related_name='search_product_requests', null=True,
        verbose_name=_("Owner"))
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True, db_index=True)
    search_request = models.ForeignKey(SearchRequest, verbose_name = _('Search request'), blank=True, null=True)
    state = models.CharField(max_length=25, choices=SEARCH_REQUEST_STATES, default='pending')

    def __unicode__(self):
        return u'%s - %s - %s - %s' % (self.category, self.piece, self.quantity,
            self.comments)
