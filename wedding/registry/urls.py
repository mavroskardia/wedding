from django.conf.urls import patterns, include, url

import registry.views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', registry.views.ActivityListView.as_view(), name='main'),
    url(r'^pledge/', registry.views.PledgeView.as_view(), name='pledge'),
    url(r'^update_ajax/', registry.views.UpdateAjaxView.as_view(), name='update_ajax'),
    url(r'^commit/', registry.views.CommitPledgeView.as_view(), name='commit'),
    # url(r'^blog/', include('blog.urls')),
)
