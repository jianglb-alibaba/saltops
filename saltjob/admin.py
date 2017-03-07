#!  /usr/bin/python
# coding=utf-8

from django.contrib import admin

from kombu.transport.django import models as kombu_models

# 注册Celery Admin模块
admin.site.register(kombu_models.Message)
