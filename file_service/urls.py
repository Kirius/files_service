# coding=utf-8
from django.conf.urls import patterns, include, url
# from django.contrib import admin
from files.views import FilesList, FilesDetail, Cabinet, ServeFile

urlpatterns = patterns(
    '',
    url(r'^$', Cabinet.as_view(), name='cabinet'),
    url(r'^files$', FilesList.as_view(), name='files_list'),
    url(r'^files/(?P<id>\d+)$', FilesDetail.as_view(), name='files_detail'),
    url(r'^s/(?P<md5>[a-f\d]{32})/(?P<name>.*)$', ServeFile.as_view(),
        name='serve_file'),
    url(r'^auth/', include('auth.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
