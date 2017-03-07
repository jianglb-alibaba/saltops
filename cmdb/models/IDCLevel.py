#!  /usr/bin/python
# coding=utf-8
from django.db import models

from common.models import BaseModel


class IDCLevel(BaseModel):
    name = models.CharField(max_length=255, verbose_name='名称')
    comment = models.TextField(verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机房等级"
        verbose_name_plural = verbose_name
