#!  /usr/bin/python
# coding=utf-8

from django.db import models
from common.models import BaseModel
from deploy_manager.models.ProjectVersion import ProjectVersion

DEPLOY_STATUS = (
    (0, '部署中'),
    (1, '部署完成'),
    (2, '部署失败'),
)


class DeployJob(BaseModel):
    project_version = models.ForeignKey(ProjectVersion, verbose_name='版本')
    job_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="作业名称")
    deploy_status = models.IntegerField(null=True, blank=True, verbose_name="部署状态", choices=DEPLOY_STATUS,
                                        default=0)

    def __str__(self):
        return self.job_name

    class Meta:
        verbose_name = "历史作业"
        verbose_name_plural = verbose_name
