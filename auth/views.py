# coding=utf-8
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('files_list')
        else:
            return render(request, 'auth/register.html', {'form': form})

    form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})
