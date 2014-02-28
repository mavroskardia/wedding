from django.conf.urls import patterns, include, url

import main.urls
import rsvp.urls
import registry.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wedding.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(main.urls)),
    url(r'^rsvp/', include(rsvp.urls)),
    url(r'^registry/', include(registry.urls, namespace='registry')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
)
