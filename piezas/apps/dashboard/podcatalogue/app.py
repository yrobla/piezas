from django.conf.urls import patterns, url
from oscar.apps.dashboard.catalogue.app import CatalogueApplication as CoreCatalogueApplication
import views

class CatalogueApplication(CoreCatalogueApplication):
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

    default_permissions = ['is_staff', ]
    permissions_map = _map = {
        'catalogue-brand': (['is_staff'], ['partner.dashboard_access']),
        'catalogue-brand-create': (['is_staff'],
                                     ['partner.dashboard_access']),
        'catalogue-brand-list': (['is_staff'], ['partner.dashboard_access']),
        'catalogue-brand-delete': (['is_staff'],
                                     ['partner.dashboard_access']),
        'model-brand': (['is_staff'], ['partner.dashboard_access']),
        'model-brand-create': (['is_staff'],
                                     ['partner.dashboard_access']),
        'model-brand-list': (['is_staff'], ['partner.dashboard_access']),
        'model-brand-delete': (['is_staff'],
                                     ['partner.dashboard_access']),
    }

    def get_urls(self):
        urls = super(CatalogueApplication, self).get_urls()

        # add new urls
        urls += [
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
            url(r'^,model/create/$',
                self.model_create_view.as_view(),
                name='catalogue-model-create'),
            url(r'^models/(?P<pk>\d+)/delete/$',
                self.model_delete_view.as_view(),
                name='catalogue-model-delete'),
            url(r'^models/(?P<pk>\d+)/update/$',
                self.model_update_view.as_view(),
                name='catalogue-brand-update'),

        ]
        return self.post_process_urls(patterns('', *urls))

application = CatalogueApplication()
