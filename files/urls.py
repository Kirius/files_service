# coding=utf-8
from django.conf.urls import patterns, url
from files.views import FilesList


urlpatterns = patterns(
    'files.views',
    url(r'$', FilesList.as_view(), name='files_list'),
)
