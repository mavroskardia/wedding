from django.conf.urls import patterns, include, url

import registry.views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', registry.views.ActivityListView.as_view(), name='main'),
    url(r'^pledge/', registry.views.PledgeView.as_view(), name='pledge'),
    # url(r'^blog/', include('blog.urls')),
)
