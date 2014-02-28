from django.conf.urls import patterns, include, url

import registry.views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', registry.views.ActivityListView.as_view(), name='main'),
    # url(r'^blog/', include('blog.urls')),    
)
