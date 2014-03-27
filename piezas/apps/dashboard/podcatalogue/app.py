from django.conf.urls import patterns, url
from oscar.apps.dashboard.catalogue.app import CatalogueApplication as CoreCatalogueApplication
from oscar.apps.dashboard.catalogue import views as coreviews
import views

class CatalogueApplication(CoreCatalogueApplication):
    # product
    product_list_view = coreviews.ProductListView
    product_lookup_view = coreviews.ProductLookupView
    product_create_redirect_view = coreviews.ProductCreateRedirectView
    product_createupdate_view = views.ProductCreateUpdateView
    product_delete_view = coreviews.ProductDeleteView
    # category
    category_list_view = coreviews.CategoryListView
    category_detail_list_view = coreviews.CategoryDetailListView
    category_create_view = coreviews.CategoryCreateView
    category_update_view = coreviews.CategoryUpdateView
    category_delete_view = coreviews.CategoryDeleteView
    stock_alert_view = coreviews.StockAlertListView
    # brand
    brand_list_view = views.BrandListView
    brand_createupdate_view = views.BrandCreateUpdateView
    brand_create_view = views.BrandCreateView
    brand_update_view = views.BrandUpdateView
    brand_delete_view = views.BrandDeleteView
    # model
    model_list_view = views.ModelListView
    model_createupdate_view = views.ModelCreateUpdateView
    model_create_view = views.ModelCreateView
    model_update_view = views.ModelUpdateView
    model_delete_view = views.ModelDeleteView
    # version
    version_list_view = views.VersionListView
    version_createupdate_view = views.VersionCreateUpdateView
    version_create_view = views.VersionCreateView
    version_update_view = views.VersionUpdateView
    version_delete_view = views.VersionDeleteView
    # bodywork
    bodywork_list_view = views.BodyworkListView
    bodywork_createupdate_view = views.BodyworkCreateUpdateView
    bodywork_create_view = views.BodyworkCreateView
    bodywork_update_view = views.BodyworkUpdateView
    bodywork_delete_view = views.BodyworkDeleteView
    # engine
    engine_list_view = views.EngineListView
    engine_createupdate_view = views.EngineCreateUpdateView
    engine_create_view = views.EngineCreateView
    engine_update_view = views.EngineUpdateView
    engine_delete_view = views.EngineDeleteView

    default_permissions = ['is_staff', ]
    permissions_map = _map = {
        # product
        'catalogue-product': (['is_staff']),
        'catalogue-piece-create': (['is_staff']),
        'catalogue-product-list': (['is_staff']),
        'catalogue-product-delete': (['is_staff']),
        'catalogue-product-lookup': (['is_staff']),
        # brand
        'catalogue-brand': (['is_staff']),
        'catalogue-brand-create': (['is_staff']),
        'catalogue-brand-list': (['is_staff']),
        'catalogue-brand-delete': (['is_staff']),
        # model
        'catalogue-model': (['is_staff']),
        'catalogue-model-create': (['is_staff']),
        'catalogue-model-list': (['is_staff']),
        'catalogue-model-delete': (['is_staff']),
        # version
        'catalogue-version': (['is_staff']),
        'catalogue-version-create': (['is_staff']),
        'catalogue-version-list': (['is_staff']),
        'catalogue-version-delete': (['is_staff']),
        # bodywork
        'catalogue-bodywork': (['is_staff']),
        'catalogue-bodywork-create': (['is_staff']),
        'catalogue-bodywork-list': (['is_staff']),
        'catalogue-bodywork-delete': (['is_staff']),
        # engine
        'catalogue-engine': (['is_staff']),
        'catalogue-engine-create': (['is_staff']),
        'catalogue-engine-list': (['is_staff']),
        'catalogue-engine-delete': (['is_staff']),
    }

    def get_urls(self):
        # add new urls
        urls = [
            # products
            url(r'^products/create/(?P<product_class_slug>[\w-]+)/$',
                self.product_createupdate_view.as_view(),
                name='catalogue-product-create'),
            url(r'^products/(?P<pk>\d+)/$',
                self.product_createupdate_view.as_view(),
                name='catalogue-product'),
            url(r'^products/(?P<pk>\d+)/delete/$',
                self.product_delete_view.as_view(),
                name='catalogue-product-delete'),
            url(r'^$', self.product_list_view.as_view(),
                name='catalogue-product-list'),
            url(r'^stock-alerts/$', self.stock_alert_view.as_view(),
                name='stock-alert-list'),
            url(r'^product-lookup/$', self.product_lookup_view.as_view(),
                name='catalogue-product-lookup'),
            # categories
            url(r'^categories/$', self.category_list_view.as_view(),
                name='catalogue-category-list'),
            url(r'^categories/(?P<pk>\d+)/$',
                self.category_detail_list_view.as_view(),
                name='catalogue-category-detail-list'),
            url(r'^categories/create/$', self.category_create_view.as_view(),
                name='catalogue-category-create'),
            url(r'^categories/create/(?P<parent>\d+)$',
                self.category_create_view.as_view(),
                name='catalogue-category-create-child'),
            url(r'^categories/(?P<pk>\d+)/update/$',
                self.category_update_view.as_view(),
                name='catalogue-category-update'),
            url(r'^categories/(?P<pk>\d+)/delete/$',
                self.category_delete_view.as_view(),
                name='catalogue-category-delete'),
            # brands
            url(r'^brands/(?P<pk>\d+)/$',
                self.brand_createupdate_view.as_view(),
                name='catalogue-brand'),
            url(r'^brands/$', self.brand_list_view.as_view(),
                name='catalogue-brand-list'),
            url(r'^brands/create/$',
                self.brand_create_view.as_view(),
                name='catalogue-brand-create'),
            url(r'^brands/(?P<pk>\d+)/delete/$',
                self.brand_delete_view.as_view(),
                name='catalogue-brand-delete'),
            url(r'^brands/(?P<pk>\d+)/update/$',
                self.brand_update_view.as_view(),
                name='catalogue-brand-update'),
            # models
            url(r'^models/(?P<pk>\d+)/$',
                self.model_createupdate_view.as_view(),
                name='catalogue-model'),
            url(r'^models/$', self.model_list_view.as_view(),
                name='catalogue-model-list'),
            url(r'^model/create/$',
                self.model_create_view.as_view(),
                name='catalogue-model-create'),
            url(r'^models/(?P<pk>\d+)/delete/$',
                self.model_delete_view.as_view(),
                name='catalogue-model-delete'),
            url(r'^models/(?P<pk>\d+)/update/$',
                self.model_update_view.as_view(),
                name='catalogue-model-update'),
            # versions
            url(r'^versions/(?P<pk>\d+)/$',
                self.version_createupdate_view.as_view(),
                name='catalogue-version'),
            url(r'^versions/$', self.version_list_view.as_view(),
                name='catalogue-version-list'),
            url(r'^version/create/$',
                self.version_create_view.as_view(),
                name='catalogue-version-create'),
            url(r'^versions/(?P<pk>\d+)/update/$',
                self.version_update_view.as_view(),
                name='catalogue-version-update'),
            url(r'^versions/(?P<pk>\d+)/delete/$',
                self.version_delete_view.as_view(),
                name='catalogue-version-delete'),
            # bodyworks
            url(r'^bodyworks/(?P<pk>\d+)/$',
                self.bodywork_createupdate_view.as_view(),
                name='catalogue-bodywork'),
            url(r'^bodyworks/$', self.bodywork_list_view.as_view(),
                name='catalogue-bodywork-list'),
            url(r'^bodywork/create/$',
                self.bodywork_create_view.as_view(),
                name='catalogue-bodywork-create'),
            url(r'^bodyworks/(?P<pk>\d+)/update/$',
                self.bodywork_update_view.as_view(),
                name='catalogue-bodywork-update'),
            url(r'^bodyworks/(?P<pk>\d+)/delete/$',
                self.bodywork_delete_view.as_view(),
                name='catalogue-bodywork-delete'),
            # engines
            url(r'^engines/(?P<pk>\d+)/$',
                self.engine_createupdate_view.as_view(),
                name='catalogue-engine'),
            url(r'^engines/$', self.engine_list_view.as_view(),
                name='catalogue-engine-list'),
            url(r'^engine/create/$',
                self.engine_create_view.as_view(),
                name='catalogue-engine-create'),
            url(r'^engines/(?P<pk>\d+)/update/$',
                self.engine_update_view.as_view(),
                name='catalogue-engine-update'),
            url(r'^engines/(?P<pk>\d+)/delete/$',
                self.engine_delete_view.as_view(),
                name='catalogue-engine-delete'),

        ]
        return self.post_process_urls(patterns('', *urls))

application = CatalogueApplication()
