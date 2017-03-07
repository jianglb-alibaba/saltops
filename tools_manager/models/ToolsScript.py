#!  /usr/bin/python
# coding=utf-8

from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from tools_manager.models.ToolsTypes import ToolsTypes

TOOL_RUN_TYPE = (
    (0, 'SaltState'),
    (1, 'Shell'),
    # (2, 'PowerShell'),
    # (3, 'Python')
)


class ToolsScript(BaseModel):
    name = models.CharField(max_length=255, verbose_name='工具名称')
    tool_script = models.TextField(verbose_name='脚本')
    tools_type = models.ForeignKey(ToolsTypes, verbose_name='工具类型')
    tool_run_type = models.IntegerField(verbose_name='脚本类型', choices=(TOOL_RUN_TYPE), default=0)
    comment = models.TextField(verbose_name='工具说明', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "工具"
        verbose_name_plural = verbose_name

