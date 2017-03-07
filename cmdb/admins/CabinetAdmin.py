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


class IDCFilter(admin.SimpleListFilter):
    title = '机房'
    parameter_name = 'idc'

    def lookups(self, request, model_admin):
        rs = set([c for c in IDC.objects.all()])
        v = set()
        for obj in rs:
            if obj is not None:
                v.add((obj.id, obj.name))
        return v

    def queryset(self, request, queryset):
        if 'idc' in request.GET:
            idc = request.GET['idc']
            return queryset.filter(idc=idc)
        else:
            return queryset.all()


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ['name', 'idc', 'rack_count', 'create_time', 'update_time']
    search_fields = ['name']
    fk_name = 'cabinet'
    list_filter = [IDCFilter]

    def rack_count(self, obj):
        return '<a href="/admin/cmdb/rack/?q=&cabinet__id__exact=%s">%s</a>' % (obj.id, obj.rack_set.count())

    rack_count.allow_tags = True
    rack_count.short_description = '机架数量'

    inlines = [RackInline]
