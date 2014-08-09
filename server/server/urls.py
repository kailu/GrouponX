from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    url(r'^api/', include('API.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
