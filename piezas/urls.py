from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from piezas.app import application
from django.contrib import admin

import views
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', login_required(views.HomeView.as_view()), name='home'),
    # url(r'^piezas/', include('piezas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(application.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^ajaximage/', include('ajaximage.urls')),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
