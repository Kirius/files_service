# coding=utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Files, UsersFiles
from .utils import json_response, md5_for_file, save_file_to_disk
from .forms import UploadFileForm


@login_required
def cabinet(request):
    return render(request, 'files/files.html', {})


@json_response
@login_required
def files_list(request):
    user = request.user
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['file']
            limit = settings.MAX_FILES_PER_USER
            # check for limit
            if UsersFiles.objects.filter(user=user).count() >= limit:
                return {'success': False,
                        'error': 'You can store up to %s files' % limit}

            # check if this user already have a file with the same name
            if UsersFiles.objects.filter(user=user,
                                         name=upload_file.name).exists():
                return {'success': False,
                        'error': 'You already have a file with such name'}

            md5 = md5_for_file(upload_file)
            try:
                file = Files.objects.get(md5=md5)
                # file with the same content already exists
                msg = (
                    'Upload successful (file already existed at: %s)'
                    % file.created_by.username
                )
            except Files.DoesNotExist:
                # there is no file with the same content
                msg = 'Upload successful (new file created)'
                try:
                    save_file_to_disk(md5, upload_file)
                except Exception:
                    return {'success': False, 'error': 'Internal save error'}

                # create file record
                file = Files.objects.create(
                    md5=md5, size=upload_file.size, created_by=user)

            # link user to file with specified file name
            UsersFiles.objects.create(
                user=user, file=file, name=upload_file.name)

            return {'msg': msg,
                    'file': {'name': upload_file.name,
                             'size': upload_file.size}}
        else:
            return {'success': False, 'error': form.errors.popitem()[1][0]}

    elif request.method == 'GET':
        files = [user_files.to_dict()
                 for user_files in UsersFiles.objects.filter(user=user)]
        return {'files': files}
