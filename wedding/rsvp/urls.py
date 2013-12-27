from django.conf.urls import patterns, include, url

import rsvp.views

urlpatterns = patterns('',
    # Examples:
    url(r'^rsvp_ajax$', rsvp.views.rsvp_ajax, name='rsvp_ajax'),
    url(r'^rsvp_submit_ajax$', rsvp.views.rsvp_submit_ajax, name='rsvp_submit_ajax'),
    # url(r'^blog/', include('blog.urls')),
)
