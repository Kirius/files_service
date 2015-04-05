# coding=utf-8
import os
from django.conf import settings
from django.db import models, IntegrityError, transaction
from django.core.urlresolvers import reverse

from .utils import md5_for_file, save_file_to_disk, get_file_path
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
        with transaction.atomic():
            try:
                file_rec = self.get(md5=md5)
                # file already exists
                status = self._add_to_user(user, file_rec, file.name)
            except self.model.DoesNotExist:
                # file does not exist
                file_rec = self.create(md5=md5, created_by=user,
                                       creation_name=file.name, size=file.size)
                self._add_to_user(user, file_rec, file.name)
                save_file_to_disk(md5, file)
                status = FILE_CREATED

        return file_rec, status

    def _add_to_user(self, user, file, name):
        try:
            UsersFiles.objects.create(user=user, file=file, name=name)
            return FILE_EXIST
        except IntegrityError:
            return DUPLICATE_NAME

    def delete_file(self, user_file_id, user):
        """
        Deletes file link from user. If user the only owner of the file,
        then also deletes file from storage
        return: True if file deleted successfully
                False if file was not deleted
        """
        with transaction.atomic():
            try:
                user_file = (
                    UsersFiles.objects.select_related('file')
                    .get(id=user_file_id, user=user)
                )
            except UsersFiles.DoesNotExist:
                return False

            file = user_file.file
            if UsersFiles.objects.filter(file=file).count() == 1:
                # user is the only owner of a file
                user_file.delete()
                file.delete()
                file_name = get_file_path(file.md5)
                os.remove(file_name)
            else:
                # there are more than 1 owner of a file
                user_file.delete()

        return True


class Files(models.Model):
    md5 = models.CharField(max_length=32, unique=True)
    size = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+')
    creation_name = models.CharField(max_length=50)
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

    def get_absolute_url(self):
        return reverse('serve_file', kwargs={'md5': self.file.md5,
                                             'name': self.name})

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'size': self.file.size,
                'added': self.added,
                'url': self.get_absolute_url()}
