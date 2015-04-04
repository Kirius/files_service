# coding=utf-8
import os
import hashlib
from django.conf import settings


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
    file_name = os.path.join(settings.FILES_DIR, md5)
    with open(file_name, 'wb') as out_file:
        for chunk in file.chunks():
            out_file.write(chunk)
