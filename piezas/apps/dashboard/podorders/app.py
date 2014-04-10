from django.conf.urls import patterns, url
from oscar.core.application import Application
from oscar.apps.dashboard.catalogue import views as coreviews
from oscar.apps.dashboard.orders.app import OrdersDashboardApplication as OrdersCoreApplication
import views

class OrdersDashboardApplication(OrdersCoreApplication):
    # search request
    searchrequest_list_view = views.SearchrequestListView
    searchrequest_detail_view = views.SearchrequestDetailView

    quote_list_view = views.QuoteListView
    quote_detail_view = views.QuoteDetailView

    default_permissions = ['is_staff', ]
    permissions_map = _map = {
        # search request
        'order-searchrequest-list': (['is_staff']),
        'searchrequest-detail': (['is_staff']),
        'quote-list': (['is_staff']),
        'quote-detail': (['is_staff']),
    }

    def get_urls(self):
        # add new urls
        urls = [
            url(r'^searchrequests/$', self.searchrequest_list_view.as_view(),
                name='order-searchrequest-list'),
            url(r'^searchrequest/(?P<number>[-\w]+)/$',
                self.searchrequest_detail_view.as_view(), name='searchrequest-detail'),
            url(r'^quotes/$', self.quote_list_view.as_view(),
                name='quote-list'),
            url(r'^quote/(?P<number>[-\w]+)/$',
                self.quote_detail_view.as_view(), name='quote-detail'),
        ]
        urls += super(OrdersDashboardApplication, self).get_urls()
        return self.post_process_urls(patterns('', *urls))

application = OrdersDashboardApplication()
