# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import login

from files.utils import login_forbidden


urlpatterns = patterns(
    'django.contrib.auth.views',
    url(r'^login/$', login_forbidden(login),
        {'template_name': 'auth/login.html'}, name='login'),
    url(r'^logout/$', 'logout_then_login', name='logout'),
)

urlpatterns += patterns(
    'auth.views',
    url(r'^register/$', 'register', name='register'),
)
