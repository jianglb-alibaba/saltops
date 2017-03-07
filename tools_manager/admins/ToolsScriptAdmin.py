#!  /usr/bin/python
# coding=utf-8
from django import forms
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from searchableselect.widgets import SearchableSelect

from cmdb.models import Host
from saltjob.tasks import execTools, scanProjectConfig
from tools_manager.models import *


@admin.register(ToolsScript)
class ToolsScriptAdmin(admin.ModelAdmin):
    list_display = ['name', 'tools_type', 'tool_run_type', 'comment', 'create_time', 'update_time', 'lastExecHistory']
    search_fields = ['name']
    list_filter = ['tools_type', 'tool_run_type']

    change_form_template = 'tools_script_change_form.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['hostList'] = Host.objects.all()
        extra_context['is_edit'] = True

        return super(ToolsScriptAdmin, self).change_view(request, object_id=object_id, form_url=form_url,
                                                         extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        obj.save()
        if request.POST['action'] == '1':
            execTools(obj, request.POST.getlist('sls_hosts'), request.POST['txt_param'])
            self.message_user(request, "工具执行成功")

    def lastExecHistory(self, obj):
        list = ToolsExecJob.objects.filter(tools=obj).order_by('-create_time')
        if len(list) > 0:
            obj = list[0]
            return '<a href="/admin/tools_manager/toolsexecjob/%s/change/">执行结果</a>' % obj.id
        else:
            return '-'

    lastExecHistory.allow_tags = True
    lastExecHistory.short_description = '执行结果'
