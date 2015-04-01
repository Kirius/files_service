# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'auth/login.html'},
        name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
)

urlpatterns += patterns(
    'auth.views',
    url(r'^register/$', 'register', name='register'),
)
