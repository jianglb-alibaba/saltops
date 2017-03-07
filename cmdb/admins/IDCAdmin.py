#!  /usr/bin/python
# coding=utf-8

import requests
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from cmdb.admins import HostAdmin
from cmdb.models import *
from deploy_manager.models import *
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltjob.tasks import scanHostJob
from saltops.settings import SALT_CONN_TYPE, SALT_HTTP_URL, SALT_REST_URL

class RackInline(NestedStackedInline):
    model = Rack
    fields = ['name']
    verbose_name = '机架'
    verbose_name_plural = '机架'
    extra = 0
    fk_name = 'cabinet'


class CabinetInline(NestedStackedInline):
    model = Cabinet
    fields = ['name']
    verbose_name = '机柜'
    verbose_name_plural = '机柜'
    extra = 0
    fk_name = 'idc'
    inlines = [RackInline]


@admin.register(IDC)
class IDCAdmin(NestedModelAdmin):
    list_display = ['name', 'type', 'phone',
                    'linkman', 'address',
                    'operator', 'concat_email', 'cabinet_count', 'create_time', 'update_time']
    search_fields = ['name']
    inlines = [CabinetInline]
    list_filter = ['type']

    def cabinet_count(self, obj):
        return '<a href="/admin/cmdb/cabinet/?q=&idc=%s">%s</a>' % (obj.id, obj.cabinet_set.count())

    cabinet_count.short_description = '机柜数量'
    cabinet_count.allow_tags = True
