#!  /usr/bin/python
# coding=utf-8

from django.db import models

from cmdb.models import Host
from common.models import BaseModel


class ToolsTypes(BaseModel):
    name = models.CharField(max_length=255, verbose_name='类型名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "工具类型"
        verbose_name_plural = verbose_name
