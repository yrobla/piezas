from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from oscar.apps.basket.app import BasketApplication as CoreBasketApplication

class BasketApplication(CoreBasketApplication):
    def get_urls(self):
        urls = [
            url(r'^$', login_required(self.summary_view.as_view()), name='summary'),
            url(r'^add/$', login_required(self.add_view.as_view()), name='add'),
            url(r'^vouchers/add/$', login_required(self.add_voucher_view.as_view()),
                name='vouchers-add'),
            url(r'^vouchers/(?P<pk>\d+)/remove/$',
                login_required(self.remove_voucher_view.as_view()), name='vouchers-remove'),
            url(r'^saved/$', login_required(self.saved_view.as_view()),
                name='saved'),
        ]
        return self.post_process_urls(patterns('', *urls))


application = BasketApplication()

