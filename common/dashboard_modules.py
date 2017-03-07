import json

from django.db.models import Count
from jet.dashboard.modules import DashboardModule
import platform
import psutil

from cmdb.models import Host
from deploy_manager.models import Project


class OverView(DashboardModule):
    title = '基础信息'
    title_url = '#'
    template = 'overview.html'

    def init_with_context(self, context):
        upMinionCount = Host.objects.filter(minion_status=1).count()
        downMinionCount = Host.objects.filter(minion_status=0).count()
        self.hostname = platform.node()
        self.system_info = '%s, %s, %s' % (
            platform.system(),
            ' '.join(platform.linux_distribution()),
            platform.release())
        self.arch = ' '.join(platform.architecture())
        self.procesor = platform.processor(),
        self.py_version = platform.python_version()
        self.host_count = Host.objects.count()
        self.buss_count = Project.objects.count()
        self.minions_status = '运行中 %s,未运行 %s' % (upMinionCount, downMinionCount)


class HostResourceOverView(DashboardModule):
    title = '资源使用率'
    title_url = '#'
    template = 'host_resource_overview.html'

    def init_with_context(self, context):
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        green, orange, red, grey = '#00FF38', '#FFB400', '#FF3B00', '#EBEBEB'

        ram_color = green
        if ram >= 75:
            ram_color = red
        elif ram >= 50:
            ram_color = orange

        cpu_color = green
        if cpu >= 75:
            cpu_color = red
        elif cpu >= 50:
            cpu_color = orange

        self.cpu_idel = 100 - cpu
        self.cpu_color = cpu_color
        self.cpu = cpu
        self.ram = 100 - ram
        self.ram_used = ram
        self.ram_color = ram_color

    class Media:
        js = ('admin/js/jquery.js', 'js/highcharts.js',)


class HostTypeOverView(DashboardModule):
    title = '操作系统分布'
    title_url = '#'
    template = 'host_type_overview.html'

    def init_with_context(self, context):
        result = Host.objects.values('os').annotate(total=Count('os'))

        os = []
        total = []
        for obj in result:
            os.append(obj['os'])
            total.append(obj['total'])
        self.os = os
        self.total = total

        class Media:
            js = ('admin/js/jquery.js', 'js/highcharts.js',)
