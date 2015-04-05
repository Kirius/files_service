# coding=utf-8
import mimetypes
import os

from django.conf import settings
from django.http import JsonResponse, FileResponse, Http404
from django.utils.http import urlencode
from django.views.generic import View, TemplateView

from .models import Files, UsersFiles
from .forms import UploadFileForm
from .utils import LoginRequiredMixin, get_file_path
from .statuses import *


class Cabinet(LoginRequiredMixin, TemplateView):
    template_name = 'files/files.html'


class FilesList(LoginRequiredMixin, View):
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


class FilesDetail(LoginRequiredMixin, View):
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


class ServeFile(View):
    def get(self, request, md5, name):
        if not settings.DEBUG:
            raise Http404()

        file_path = get_file_path(md5)
        statobj = os.stat(file_path)
        content_type = 'application/octet-stream'
        response = FileResponse(open(file_path, 'rb'),
                                content_type=content_type)

        response["Content-Length"] = statobj.st_size
        return response
