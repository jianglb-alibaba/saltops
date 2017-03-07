#!  /usr/bin/python
# coding=utf-8
from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from tools_manager.models.ToolsScript import ToolsScript


class ToolsExecJob(BaseModel):
    tools = models.ForeignKey(ToolsScript, verbose_name='工具')
    hosts = models.ManyToManyField(Host, verbose_name='目标主机')
    param = models.TextField(verbose_name='执行参数', blank=True, null=True, default="")

    def __str__(self):
        return self.param

    class Meta:
        verbose_name = "执行记录"
        verbose_name_plural = verbose_name

