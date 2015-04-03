# coding=utf-8
import os
import hashlib
import json
from django.conf import settings
from django.http import HttpResponse


def json_response(view):
    """
    Decorator for views to return json.
    Decorated view must return a json serializable dictionary.
    """
    def _f(*args, **kwargs):
        res = view(*args, **kwargs)
        # if 'success' not in res:
        #     res['success'] = True

        return HttpResponse(json.dumps(res), content_type='application/json')

    return _f


def md5_for_file(file):
    """
    file - instance of django django.core.files.uploadedfile.UploadedFile
    Returns md5 for a file.
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
