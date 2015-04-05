# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('md5', models.CharField(unique=True, max_length=32)),
                ('size', models.PositiveIntegerField()),
                ('created_by', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('file', models.ForeignKey(to='files.Files')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-added',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='usersfiles',
            unique_together=set([('user', 'name')]),
        ),
        migrations.AddField(
            model_name='files',
            name='users',
            field=models.ManyToManyField(related_name='files', through='files.UsersFiles', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
