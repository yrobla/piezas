from django.conf.urls import patterns, url, include
from oscar.apps.dashboard.app import DashboardApplication as CoreDashboardApplication
from oscar.core.loading import get_class

class DashboardApplication(CoreDashboardApplication):
    catalogue_app = get_class('piezas.apps.dashboard.podcatalogue.app', 'application')
    orders_app = get_class('piezas.apps.dashboard.podorders.app', 'application')

application = DashboardApplication()
