#!  /usr/bin/python
# coding=utf-8

from django.contrib import admin

from cmdb.models import Cabinet
from cmdb.models import Rack


class CabinetFilter(admin.SimpleListFilter):
    title = '机柜'
    parameter_name = 'cabinet'

    def lookups(self, request, model_admin):
        rs = set([c for c in Cabinet.objects.all()])
        v = set()
        for obj in rs:
            if obj is not None:
                v.add((obj.id, obj.name))
        return v

    def queryset(self, request, queryset):
        if 'cabinet' in request.GET:
            cabinet = request.GET['cabinet']
            return queryset.filter(cabinet=cabinet)
        else:
            return queryset.all()


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['cabinet', 'name', 'create_time', 'update_time']
    search_fields = ['cabinet', 'name']
    list_filter = [CabinetFilter]
