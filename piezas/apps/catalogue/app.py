from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from oscar.apps.catalogue.app import BaseCatalogueApplication as CoreCatalogueApplication
import views

class BaseCatalogueApplication(CoreCatalogueApplication):

    product_questions_view = views.ProductQuestionsView

    def get_urls(self):
        urlpatterns = []
        urls = [
            url(r'^$', login_required(self.index_view.as_view()), name='index'),
            url(r'^(?P<product_slug>[\w-]*)_(?P<pk>\d+)/$',
                login_required(self.detail_view.as_view()), name='detail'),
            url(r'^category/(?P<category_slug>[\w-]+(/[\w-]+)*)_(?P<pk>\d+)/$',
                login_required(self.category_view.as_view()), name='category'),
            url(r'^ranges/(?P<slug>[\w-]+)/$',
                login_required(self.range_view.as_view()), name='range'),
            url(r'^productquestions/(?P<pk>\d+)/$',
                login_required(self.product_questions_view.as_view()), name='product_questions'),
            # Legacy route for the category view
            url(r'^(?P<category_slug>[\w-]+(/[\w-]+)*)/$',
                login_required(self.category_view.as_view()), name='category')]
        urlpatterns += patterns('', *urls)
        return self.post_process_urls(urlpatterns)

application = BaseCatalogueApplication()
