# coding=utf-8
from django.conf import settings
from django.db import models


class Files(models.Model):
    md5 = models.CharField(max_length=32, unique=True)
    size = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='UsersFiles', related_name='files')


class UsersFiles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    file = models.ForeignKey(Files)
    name = models.CharField(max_length=100)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')
