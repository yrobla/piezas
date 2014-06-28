from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from haystack.views import search_view_factory
from oscar.apps.search.app import SearchApplication as CoreSearchApplication
import views

class SearchApplication(CoreSearchApplication):
    index_view = views.HomeView
    confirm_view = views.ConfirmView
    placed_view = views.PlacedView
    quoteplaced_view = views.QuotePlacedView
    quote_view = views.QuoteView
    create_quote_view = views.CreateQuoteView
    pending_search_requests_view = views.PendingSearchRequestsView
    active_searches_view = views.ActiveSearchesView
    history_searches_view = views.HistorySearchesView
    expired_searches_view = views.ExpiredSearchesView
    canceled_searches_view = views.CanceledSearchesView
    received_quote_view = views.ReceivedQuotesView
    recalc_quotes_view = views.RecalcQuotesView
    recalc_quote_view = views.RecalcQuoteView
    send_recalc_quote_view = views.SendRecalcQuoteView
    cancel_view = views.CancelSearchView
    search_detail_view = views.SearchDetailView
    quote_detail_view = views.QuoteDetailView
    quote_accept_view = views.QuoteAcceptView
    quote_recalc_view = views.QuoteRecalcView
    recalcplaced_view = views.RecalcPlacedView
    cancelplaced_view = views.CancelPlacedView
    place_order_view = views.PlaceOrderView
    orderplaced_view = views.OrderPlacedView

    def get_urls(self):
        # The form class has to be passed to the __init__ method as that is how
        # Haystack works.  It's slightly different to normal CBVs.
        urlpatterns = patterns(
            '',
            url(r'^$', login_required(search_view_factory(
                view_class=self.search_view,
                form_class=self.search_form,
                searchqueryset=self.get_sqs())),
                name='search'),
            url(r'^home/$', login_required(self.index_view.as_view()), name='home'),
            url(r'^receivedquotes/$', login_required(self.received_quote_view.as_view()), name='receivedquotes'),
            url(r'^activesearches/$', login_required(self.active_searches_view.as_view()), name='activesearches'),
            url(r'^history/$', login_required(self.history_searches_view.as_view()), name='history'),
            url(r'^expiredsearches/$', login_required(self.expired_searches_view.as_view()), name='expiredsearches'),
            url(r'^canceledsearches/$', login_required(self.canceled_searches_view.as_view()), name='canceledsearches'),
            url(r'^recalcquotes/$', login_required(self.recalc_quotes_view.as_view()), name='recalcquotes'),
            url(r'^placesearch/$', login_required(self.confirm_view.as_view()), name='placesearchrequest'),
            url(r'^placed/$', login_required(self.placed_view.as_view()), name='placed'),
            url(r'^quoteplaced/$', login_required(self.quoteplaced_view.as_view()), name='quoteplaced'),
            url(r'^acceptquote/(?P<number>[\w-]*)/$', login_required(self.quote_accept_view.as_view()), name='acceptquote'),
            url(r'^cancelsearch/$', login_required(self.cancel_view.as_view()), name='cancel'),
            url(r'^confirmrecalcquote/(?P<number>[\w-]*)/$', login_required(self.quote_recalc_view.as_view()), name='confirmrecalcquote'),
            url(r'^recalcquote/$', login_required(self.recalc_quote_view.as_view()), name='recalcquote'),
            url(r'^sendrecalcquote/$', login_required(self.send_recalc_quote_view.as_view()), name='sendrecalcquote'),
            url(r'^cancelquote/$', login_required(self.recalc_quote_view.as_view()), name='cancelquote'),
            url(r'^recalcplaced/$', login_required(self.recalcplaced_view.as_view()), name='recalcplaced'),
            url(r'^sendrecalcplaced/$', login_required(self.recalcplaced_view.as_view()), name='sendrecalcplaced'),
            url(r'^cancelplaced/$', login_required(self.cancelplaced_view.as_view()), name='cancelplaced'),
            url(r'^pendingrequests/$', login_required(self.pending_search_requests_view.as_view()), name='request-list'),
            url(r'^detail/(?P<number>[\w-]*)/$', login_required(self.search_detail_view.as_view()), name='detail'),
            url(r'^quotedetail/(?P<number>[\w-]*)/$', login_required(self.quote_detail_view.as_view()), name='quotedetail'),
            url(r'^quoteview/(?P<number>[\w-]*)/$', login_required(self.quote_view.as_view()), name='quoteview'),
            url(r'^createquote/(?P<pk>[\w-]*)/$',
                login_required(self.create_quote_view.as_view()),
                name='quote'),
            url(r'^placeorder/$', login_required(self.place_order_view.as_view()), name='placeorder'),
            url(r'^orderplaced/$', login_required(self.orderplaced_view.as_view()), name='orderplaced'),
        )
        return self.post_process_urls(urlpatterns)

application = SearchApplication()
