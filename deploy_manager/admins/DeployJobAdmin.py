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


class DeployJobDetailInline(admin.StackedInline):
    model = DeployJobDetail
    fields = ['host', 'job_cmd', 'duration', 'deploy_message', 'stderr', 'comment', 'is_success']
    verbose_name = '作业详情'
    verbose_name_plural = '作业详情'
    extra = 0
    can_delete = False
    readonly_fields = ['host', 'job_cmd', 'duration', 'deploy_message', 'stderr',
                       'create_time', 'update_time', 'comment', 'is_success']
    ordering = ['-create_time']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DeployJob)
class DeployJobAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'project_version', 'create_time', 'update_time', 'deploy_status']
    readonly_fields = ['job_name', 'project_version', 'deploy_status']
    search_fields = ['job_name']
    list_filter = ['deploy_status']
    inlines = [DeployJobDetailInline]

    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = ('/static/js/DeployJobAdmin.js',)
