# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'files.views',
    url(r'$', 'files_list', name='files_list'),
)
