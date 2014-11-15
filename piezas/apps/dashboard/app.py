from django.conf.urls import patterns, url, include
from oscar.apps.dashboard.app import DashboardApplication as CoreDashboardApplication
from oscar.core.loading import get_class
from piezas.apps.dashboard.podcatalogue.app import CatalogueApplication
from piezas.apps.dashboard.podorders.app import OrdersDashboardApplication
from piezas.apps.dashboard.podusers.app import UsersDashboardApplication

class DashboardApplication(CoreDashboardApplication):
    orders_app = OrdersDashboardApplication()
    catalogue_app = CatalogueApplication()
    users_app = UsersDashboardApplication()

    def get_urls(self):
        urls = [
            url(r'^$', self.index_view.as_view(), name='index'),
            url(r'^catalogue/', include(self.catalogue_app.urls)),
            url(r'^reports/', include(self.reports_app.urls)),
            url(r'^orders/', include(self.orders_app.urls)),
            url(r'^users/', include(self.users_app.urls)),
            url(r'^content-blocks/', include(self.promotions_app.urls)),
            url(r'^pages/', include(self.pages_app.urls)),
            url(r'^partners/', include(self.partners_app.urls)),
            url(r'^offers/', include(self.offers_app.urls)),
            url(r'^ranges/', include(self.ranges_app.urls)),
            url(r'^reviews/', include(self.reviews_app.urls)),
            url(r'^vouchers/', include(self.vouchers_app.urls)),
            url(r'^comms/', include(self.comms_app.urls)),
        ]
        return self.post_process_urls(patterns('', *urls))

application = DashboardApplication()
