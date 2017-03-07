#!  /usr/bin/python
# coding=utf-8
from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from tools_manager.models.ToolsExecJob import ToolsExecJob


class ToolsExecDetailHistory(BaseModel):
    tool_exec_history = models.ForeignKey(ToolsExecJob, blank=True, null=True)
    host = models.ForeignKey(Host, verbose_name='目标主机', blank=True, null=True)
    exec_result = models.TextField(verbose_name='执行结果', blank=True, null=True, default="")
    err_msg = models.TextField(verbose_name='错误信息', blank=True, null=True, default="")

    def __str__(self):
        return self.host.host_name

    class Meta:
        verbose_name = "工具详细信息"
        verbose_name_plural = verbose_name
