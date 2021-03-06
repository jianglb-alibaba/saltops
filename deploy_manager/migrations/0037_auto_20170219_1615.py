# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 08:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy_manager', '0036_auto_20170217_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('file_path', models.FilePathField(blank=True, null=True, verbose_name='文件路径')),
                ('file_content', models.TextField(blank=True, null=True, verbose_name='配置文件')),
            ],
            options={
                'verbose_name': '主机配置信息',
                'verbose_name_plural': '主机配置信息',
            },
        ),
        migrations.CreateModel(
            name='ProjectConfigPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('config_path', models.FilePathField(blank=True, null=True, verbose_name='配置文件路径')),
            ],
            options={
                'verbose_name': '业务配置路径',
                'verbose_name_plural': '业务配置路径',
            },
        ),
        migrations.AlterField(
            model_name='projectversion',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='D:\\github\\saltops\\doc\\scripts\\', verbose_name='版本'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_config_path',
            field=models.ManyToManyField(blank=True, null=True, to='deploy_manager.ProjectConfigPath', verbose_name='业务配置文件'),
        ),
        migrations.AddField(
            model_name='projecthost',
            name='config',
            field=models.ManyToManyField(to='deploy_manager.ProjectConfig', verbose_name='配置文件'),
        ),
    ]
