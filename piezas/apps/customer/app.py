from django.conf.urls import patterns, url
from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication
import views


class CustomerApplication(CoreCustomerApplication):
    login_view = views.PodAccountAuthView
    profile_view = views.ProfileView


application = CustomerApplication()
