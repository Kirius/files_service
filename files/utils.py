# coding=utf-8
import os
import hashlib

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def get_file_path(md5):
    return os.path.join(settings.FILES_DIR, md5)


def md5_for_file(file):
    """
    file: instance of django django.core.files.uploadedfile.UploadedFile
    returns: md5 for a file.
    """
    md5 = hashlib.md5()
    for data in file.chunks():
        md5.update(data)
    return md5.hexdigest()


def save_file_to_disk(md5, file):
    """
    md5: md5 checksum for a file.
    file: instance of django django.core.files.uploadedfile.UploadedFile
    """
    with open(get_file_path(md5), 'wb') as out_file:
        for chunk in file.chunks():
            out_file.write(chunk)


def login_forbidden(view):
    """
    Decorator for views that checks that the user is logged out, redirecting
    to the cabinet if necessary.
    """
    def _f(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('cabinet')
        else:
            return view(request, *args, **kwargs)
    return _f


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
