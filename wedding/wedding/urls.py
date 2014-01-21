from django.conf.urls import patterns, include, url

import main.urls
import rsvp.urls
import roomshare.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wedding.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(main.urls)),
    url(r'^rsvp/', include(rsvp.urls)),
    url(r'^roomshare/', include(roomshare.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
