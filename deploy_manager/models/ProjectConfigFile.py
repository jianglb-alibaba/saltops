#!  /usr/bin/python
# coding=utf-8

from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from deploy_manager.models import *


class ProjectConfigFile(BaseModel):
    project = models.ForeignKey(Project, verbose_name='业务', null=True)
    config_path = models.CharField(max_length=255, verbose_name='配置文件路径', blank=True, null=True)

    def __str__(self):
        return self.config_path

    class Meta:
        verbose_name = "业务配置"
        verbose_name_plural = verbose_name
