#!  /usr/bin/python
# coding=utf-8

from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from common.models import BaseModel


class ProjectModule(MPTTModel, BaseModel):
    """
    业务模块
    """
    parent = TreeForeignKey('self', verbose_name='上级业务模块',
                            null=True, blank=True, related_name='children', db_index=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="业务模块名称")

    class MPTTMeta:
        parent_attr = 'parent'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "业务模块"
        verbose_name_plural = verbose_name
