#!  /usr/bin/python
# coding=utf-8

from django.contrib.auth.models import User
from django.db import models

from cmdb.models import Host
from common.models import BaseModel
from deploy_manager.models.ProjectModule import ProjectModule

JOB_SCRIPT_TYPE = (
    (100, '----'),
    (0, 'sls'),
    (1, 'shell'),
)


class Project(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="业务名称")
    host = models.ManyToManyField(Host, default="", verbose_name="主机",
                                  blank=True, through='ProjectHost')
    project_module = models.ForeignKey(ProjectModule, verbose_name='业务模块', blank=True, null=True, default="")
    job_script_type = models.IntegerField(default=0, choices=JOB_SCRIPT_TYPE,
                                          verbose_name='脚本语言')
    playbook = models.TextField(verbose_name='部署脚本', null=True, blank=True,
                                help_text='${version}代表默认版本号')
    anti_install_playbook = models.TextField(verbose_name='卸载脚本', null=True, blank=True,
                                             help_text='${version}代表默认版本号')
    extra_param = models.TextField(verbose_name='扩展参数', default="", blank=True, null=True)
    dev_monitor = models.ForeignKey(User, verbose_name='开发负责人', blank=True, null=True, related_name='dev_monitor')
    ops_monitor = models.ForeignKey(User, verbose_name='运维负责人', blank=True, null=True, related_name='ops_monitor')
    backup_monitor = models.ForeignKey(User, verbose_name='备份负责人', blank=True, null=True, related_name='backup_monitor')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "业务"
        verbose_name_plural = verbose_name
