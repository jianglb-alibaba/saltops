#!  /usr/bin/python
# coding=utf-8

from django.contrib import admin

from cmdb.models import ISP


@admin.register(ISP)
class ISPAdmin(admin.ModelAdmin):
    list_display = ['name', 'create_time', 'update_time']
    search_fields = ['name']