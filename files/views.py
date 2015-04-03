# coding=utf-8
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
    if request.method == 'POST':
        user = request.user
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['file']
            md5 = md5_for_file(upload_file)
            try:
                file = Files.objects.get(md5=md5)
            except Files.DoesNotExist:
                try:
                    save_file_to_disk(md5, upload_file)
                except Exception:
                    return {'success': False, 'errors': 'Internal save error'}

                file = Files.objects.create(
                    md5=md5, size=upload_file.size, created_by=user)

            UsersFiles.objects.create(
                user=user, file=file, name=upload_file.name)

            return {'success': True, 'name': upload_file.name}
        else:
            return {'success': False, 'errors': form.errors}

    return {'files': ['file1', 'file2', 'file3']}
