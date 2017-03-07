#!  /usr/bin/python
# coding=utf-8

import requests
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from cmdb.models import *
from deploy_manager.models import *
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltjob.tasks import scanHostJob
from saltops.settings import SALT_CONN_TYPE, SALT_HTTP_URL, SALT_REST_URL


class IPInline(admin.TabularInline):
    model = HostIP
    fields = ['ip', 'ip_type']
    verbose_name = "IP"
    verbose_name_plural = "IP"
    extra = 0


class ProjectInline(admin.TabularInline):
    model = Project.host.through
    fields = ['project']
    verbose_name = '业务'
    verbose_name_plural = '业务'
    extra = 0


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^scan_host/$',
                self.admin_site.admin_view(self.scan_host),
                name='scan_host',
            ),
        ]
        return custom_urls + urls

    list_display = ['host_name', 'kernel',
                    'host', 'idc', 'system_serialnumber',
                    'os', 'virtual', 'enable_ssh', 'minion_status', 'create_time', 'update_time']
    search_fields = ['host']
    list_filter = ['virtual', 'os_family',  'minion_status']
    inlines = [IPInline, ProjectInline]
    change_list_template = 'cmdb_host_list.html'

    def scan_host(self, request):
        scanHostJob()
        self.message_user(request, "主机扫描完成")
        return super(HostAdmin, self).changelist_view(request=request)

    # def acceptAction(self, request, queryset):
    #     for obj in queryset:
    #         salt_api_token({'fun': 'key.accept', 'match': obj.host_name},
    #                        SALT_REST_URL, {'X-Auth-Token': token_id()}).wheelRun()
    #         self.message_user(request, "%s 个客户端接受成功" % len(queryset))
    #
    # acceptAction.short_description = "接受客户端"
    #
    # actions = [acceptAction, ]

    def save_formset(self, request, form, formset, change):
        entity = form.save()
        formset.save()
        # 如果主机是SSH类型的，把SSH列表更新一遍
        if entity.enable_ssh is True:
            hosts = Host.objects.all()

            rosterString = ""
            for host in hosts:
                if host.enable_ssh is True:
                    rosterString += """

%s:
    host: %s
    user: %s
    passwd: %s
    sudo: %s
    tty: True

                """ % (host.host, host.host, host.ssh_username, host.ssh_password,
                       host.enable_ssh)

            if SALT_CONN_TYPE == 'http':
                requests.post(SALT_HTTP_URL + '/rouster', data={'content': rosterString})
            else:
                with open('/etc/salt/roster', 'w') as content:
                    content.write(rosterString)
