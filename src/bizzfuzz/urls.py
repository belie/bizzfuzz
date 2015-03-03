from django.conf.urls import patterns, include, url
from django.contrib import admin
from bizzfuzzUI.views import UserListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bizzfuzz.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', UserListView.as_view(), name='list_user'),
    url(r'^bizzfuzz/', include('bizzfuzzUI.urls', namespace="bizzfuzz")),
    url(r'^admin/', include(admin.site.urls)),
)
