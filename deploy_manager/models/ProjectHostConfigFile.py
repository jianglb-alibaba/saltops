#!  /usr/bin/python
# coding=utf-8

from django.db import models
from cmdb.models import Host
from common.models import BaseModel
from deploy_manager.models import ProjectHost


class ProjectHostConfigFile(BaseModel):
    project_host = models.ForeignKey(ProjectHost, verbose_name='业务')
    file_path = models.CharField(verbose_name='配置路径', max_length=255, null=True, blank=True)
    file_content = models.TextField(verbose_name='配置内容', null=True, blank=True)

    def __str__(self):
        return self.file_path

    class Meta:
        verbose_name = "配置内容"
        verbose_name_plural = verbose_name
