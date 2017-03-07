#!  /usr/bin/python
# coding=utf-8


from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from searchableselect.widgets import SearchableSelect

from saltjob.tasks import execTools
from tools_manager.models import *


@admin.register(ToolsTypes)
class ToolsTypesAdmin(admin.ModelAdmin):
    list_display = ['name', 'script_count', 'create_time', 'update_time']
    search_fields = ['name']

    def script_count(self, obj):
        return '<a href="/admin/tools_manager/toolsscript/?q=&tools_type__id__exact=%s">%s</a>' % (
            obj.id, obj.toolsscript_set.count())

    script_count.short_description = '工具数量'
    script_count.allow_tags = True

