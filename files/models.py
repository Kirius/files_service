# coding=utf-8
from django.conf import settings
from django.db import models
from django.db import IntegrityError

from files.utils import md5_for_file, save_file_to_disk
from .statuses import *


class FilesManager(models.Manager):

    def create_file(self, file, user):
        """
        Creates file for a user. If file with the same content already exists,
        only link is created.

        file: instance of django django.core.files.uploadedfile.UploadedFile
        user: user who attempts to create file
        returns: tuple of (Files model instance, status)
        """
        md5 = md5_for_file(file)
        try:
            file_rec = self.get(md5=md5)
            status = self._add_to_user(user, file_rec, file.name)
        except self.model.DoesNotExist:
            status = FILE_CREATED
            save_file_to_disk(md5, file)
            file_rec = self.create(md5=md5, size=file.size, created_by=user)
            self._add_to_user(user, file_rec, file.name)

        return file_rec, status

    def _add_to_user(self, user, file, name):
        try:
            UsersFiles.objects.create(user=user, file=file, name=name)
            return FILE_EXIST
        except IntegrityError:
            return DUPLICATE_NAME


class Files(models.Model):
    md5 = models.CharField(max_length=32, unique=True)
    size = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='UsersFiles', related_name='files')
    objects = FilesManager()

    def user_file(self, user, name):
        return UsersFiles.objects.get(user=user, file=self, name=name)


class UsersFiles(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    file = models.ForeignKey(Files)
    name = models.CharField(max_length=50)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ('-added',)

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'size': self.file.size}
