import django
from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from oscar.core.application import Application
from oscar.apps.customer import forms
from oscar.core.loading import get_class
from oscar.views.decorators import login_forbidden

from oscar.app import Shop
import views

class PodApplication(Shop):
    index_view = views.HomeView

    def get_urls(self):
        urls = super(PodApplication, self).get_urls()

        urls += [
            url(r'^home/', self.index_view.as_view(), name='index'),
        ]
        return patterns('', *urls)

application = PodApplication()
