#!  /usr/bin/python
# coding=utf-8


from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from mptt.admin import MPTTModelAdmin

from deploy_manager.models import *
from saltjob.tasks import deployTask


class ProjectModuleFilter(admin.SimpleListFilter):
    title = '上级业务模块'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        rs = set([c.parent for c in ProjectModule.objects.all()])
        v = set()
        for obj in rs:
            if obj is not None:
                v.add((obj.id, obj.name))
        return v

    def queryset(self, request, queryset):
        if 'parent' in request.GET:
            parentid = request.GET['parent']
            return queryset.filter(parent=parentid)
        else:
            return queryset.all()


@admin.register(ProjectModule)
class ProjectModuleAdmin(MPTTModelAdmin):
    list_display = ['name', 'parent', 'create_time', 'update_time']
    search_fields = ['name']
    list_filter = [ProjectModuleFilter, ]
