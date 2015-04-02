# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from files.utils import json_response
from .forms import UploadFileForm


def handle_uploaded_file(f):
    with open('/home/kir/projects/learning/file_service/media/1.txt', 'wb+') as d:
        for chunk in f.chunks():
            d.write(chunk)


@login_required
def cabinet(request):
    return render(request, 'files/files.html', {})


@json_response
@login_required
def files_list(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return {'name': 'name1'}

    return {'files': ['file1', 'file2', 'file3']}
