from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from haystack.views import search_view_factory
from oscar.apps.search.app import SearchApplication as CoreSearchApplication
import views

class SearchApplication(CoreSearchApplication):
    index_view = views.HomeView
    confirm_view = views.ConfirmView
    placed_view = views.PlacedView

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
            url(r'^placesearch/$', login_required(self.confirm_view.as_view()), name='placesearchrequest'),
            url(r'^placed/$', login_required(self.placed_view.as_view()), name='placed'),
            url(r'^pendingrequests/$', login_required(self.placed_view.as_view()), name='request-list'),
        )
        return self.post_process_urls(urlpatterns)

application = SearchApplication()
