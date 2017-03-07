#!  /usr/bin/python
# coding=utf-8

from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from deploy_manager.models.DeployJob import DeployJob


class DeployJobDetail(BaseModel):
    host = models.ForeignKey(Host, verbose_name='主机名')
    deploy_message = models.TextField(verbose_name='作业信息', blank=True, null=True)
    job = models.ForeignKey(DeployJob, verbose_name='作业名称', blank=True, null=True)

    job_cmd = models.TextField(blank=True, null=True, verbose_name="作业命令")
    start_time = models.DateTimeField(verbose_name='开始时间', blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='执行时长', blank=True, null=True)
    stderr = models.TextField(blank=True, null=True, verbose_name="其他信息")
    comment = models.TextField(blank=True, null=True, verbose_name="提示信息", default="")
    is_success = models.BooleanField(choices=((True, '执行成功'), (False, '执行失败')), verbose_name='执行情况', default=True)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = "部署详情"
        verbose_name_plural = verbose_name
