from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from oscar.apps.offer.app import OfferApplication as CoreOfferApplication

class OfferApplication(CoreOfferApplication):

    def get_urls(self):
        urls = [
            url(r'^$', login_required(self.list_view.as_view()), name='list'),
            url(r'^(?P<slug>[\w-]+)/$', login_required(self.detail_view.as_view()),
                name='detail'),
        ]
        return self.post_process_urls(patterns('', *urls))

application = OfferApplication()
