# coding=utf-8
from django.conf.urls import patterns, include, url
# from django.contrib import admin
from django.views.static import serve
from files.views import FilesList, FilesDetail, Cabinet

urlpatterns = patterns(
    '',
    url(r'^$', Cabinet.as_view(), name='cabinet'),
    url(r'^files$', FilesList.as_view(), name='files_list'),
    url(r'^files/(?P<id>\d+)$', FilesDetail.as_view(), name='files_detail'),
    url(r'^auth/', include('auth.urls')),
    # url(r'^admin/', include(admin.site.urls)),
)
