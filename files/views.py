# coding=utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from .models import Files, UsersFiles
from .forms import UploadFileForm
from .statuses import *


@login_required
def cabinet(request):
    return render(request, 'files/files.html', {})


# @json_response
# @login_required
# def files_list(request):
#     user = request.user
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             upload_file = request.FILES['file']
#             limit = settings.MAX_FILES_PER_USER
#             # check for limit
#             if UsersFiles.objects.filter(user=user).count() >= limit:
#                 return {'success': False,
#                         'error': 'You can store up to %s files' % limit}
#
#             try:
#                 file, status = Files.objects.create_file(upload_file, user)
#             except Exception:
#                 return {'success': False, 'error': 'Internal storage error'}
#
#             if status == FILE_CREATED:
#                 msg = 'Upload successful (new file created)'
#             elif status == FILE_EXIST:
#                 msg = ('Upload successful (file already existed at: %s)'
#                        % file.created_by.username)
#             else:
#                 error = 'You already have a file with such name'
#                 return {'success': False, 'error': error}
#
#             return {'msg': msg,
#                     'file': file.user_file(user, upload_file.name).to_dict()}
#         else:
#             return {'success': False, 'error': form.errors.popitem()[1][0]}
#
#     elif request.method == 'GET':
#         files = [user_files.to_dict()
#                  for user_files in UsersFiles.objects.filter(user=user)]
#         return {'files': files}


class FilesList(View):
    def get(self, request):
        files = [user_file.to_dict() for user_file
                 in UsersFiles.objects.select_related('file')
                 .filter(user=request.user)]

        return JsonResponse({'files': files})

    def post(self, request):
        user = request.user
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['file']
            limit = settings.MAX_FILES_PER_USER
            # check for limit
            if UsersFiles.objects.filter(user=user).count() >= limit:
                data = {'error': 'You can store up to %s files' % limit}
                return JsonResponse(data, status=HTTP_BAD_REQUEST_400)

            try:
                file, status = Files.objects.create_file(upload_file, user)
            except Exception:
                data = {'error': 'Internal storage error'}
                return JsonResponse(data, status=HTTP_SERVER_ERROR_500)

            if status == FILE_CREATED:
                msg = 'Upload successful (new file created)'
            elif status == FILE_EXIST:
                msg = ('Upload successful (file already existed at: %s)'
                       % file.created_by.username)
            else:
                data = {'error': 'You already have a file with such name'}
                return JsonResponse(data, HTTP_BAD_REQUEST_400)

            data = {'msg': msg,
                    'file': file.user_file(user, upload_file.name).to_dict()}

            return JsonResponse(data, status=HTTP_CREATED_201)
        else:
            data = {'error': form.errors.popitem()[1][0]}
            return JsonResponse(data, status=HTTP_BAD_REQUEST_400)


class FilesDetail(View):
    def delete(self, request, id):
        try:
            deleted = Files.objects.delete_file(id, request.user)
        except Exception:
            data = {'error': 'Internal storage error'}
            return JsonResponse(data, status=HTTP_SERVER_ERROR_500)

        if deleted:
            return JsonResponse({}, status=HTTP_SUCCESS_204)
        else:
            data = {'error': 'Invalid request'}
            return JsonResponse(data, status=HTTP_BAD_REQUEST_400)
