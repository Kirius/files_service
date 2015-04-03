# coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.static import serve

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'files.views.cabinet', name='cabinet'),
    url(r'^auth/', include('auth.urls')),
    url(r'^files/', include('files.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
