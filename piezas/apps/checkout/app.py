from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from oscar.apps.checkout.app import CheckoutApplication as CoreCheckoutApplication

class CheckoutApplication(CoreCheckoutApplication):
    def get_urls(self):
        urls = [
            url(r'^$', login_required(self.index_view.as_view()), name='index'),

            # Shipping/user address views
            url(r'shipping-address/$',
                login_required(self.shipping_address_view.as_view()), name='shipping-address'),
            url(r'user-address/edit/(?P<pk>\d+)/$',
                login_required(self.user_address_update_view.as_view()),
                name='user-address-update'),
            url(r'user-address/delete/(?P<pk>\d+)/$',
                login_required(self.user_address_delete_view.as_view()),
                name='user-address-delete'),

            # Shipping method views
            url(r'shipping-method/$',
                login_required(self.shipping_method_view.as_view()), name='shipping-method'),

            # Payment method views
            url(r'payment-method/$',
                login_required(self.payment_method_view.as_view()), name='payment-method'),
            url(r'payment-details/$',
                login_required(self.payment_details_view.as_view()), name='payment-details'),

            # Preview and thankyou
            url(r'preview/$',
                login_required(self.payment_details_view.as_view(preview=True)),
                name='preview'),
            url(r'thank-you/$', login_required(self.thankyou_view.as_view()),
                name='thank-you'),
        ]
        return self.post_process_urls(patterns('', *urls))

application = CheckoutApplication()
