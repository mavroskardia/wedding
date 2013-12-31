from django.conf.urls import patterns, include, url

import main.views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', main.views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),    
)
