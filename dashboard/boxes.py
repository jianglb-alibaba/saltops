import platform
import psutil
from django.db.models import Count
from suit_dashboard.box import Box, Item

from cmdb.models import Host
from deploy_manager.models import Project


def minion_status_chart():
    result = Host.objects.values('os').annotate(total=Count('os'))

    os = []
    total = []
    for obj in result:
        os.append(obj['os'])
        total.append(obj['total'])

    chart_options = {
        'chart': {
            'height': 350,
        },
        'title': {
            'text': '操作系统分布'
        },
        'xAxis': {
            'categories': os
        },
        'series': [
            {
                'type': 'column',
                'data': total
            }],
    }
    return chart_options


def machine_usage_chart():
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

    chart_options = {
        'chart': {
            'type': 'bar',
            'height': 243,
        },
        'title': {
            'text': '资源使用率'
        },
        'xAxis': {
            'categories': ['CPU使用率', '内存使用率']
        },
        'yAxis': {
            'min': 0,
            'max': 100,
            'title': {
                'text': '百分比'
            }
        },
        'tooltip': {
            'percentageDecimals': 1
        },
        'legend': {
            'enabled': False
        },
        'plotOptions': {
            'series': {
                'stacking': 'normal'
            }
        },
        'series': [{
            'name': 'CPU idle',
            'data': [{'y': 100 - cpu, 'color': grey}, {'y': 0}],
        }, {
            'name': 'CPU used',
            'data': [{'y': cpu, 'color': cpu_color}, {'y': 0}],
        }, {
            'name': 'RAM free',
            'data': [{'y': 0}, {'y': 100 - ram, 'color': grey}],
        }, {
            'name': 'RAM used',
            'data': [{'y': 0}, {'y': ram, 'color': ram_color}],
        }]
    }
    return chart_options


class BoxMachineBasicInfo(Box):
    def get_items(self):
        upMinionCount = Host.objects.filter(minion_status=1).count()
        downMinionCount = Host.objects.filter(minion_status=0).count()

        # 系统基础信息
        item_info = Item(
            html_id='SysInfo', name='主机系统信息',
            display=Item.AS_TABLE,
            value=(
                ('系统', '%s, %s, %s' % (
                    platform.system(),
                    ' '.join(platform.linux_distribution()),
                    platform.release())),
                ('架构', ' '.join(platform.architecture())),
                ('处理器', platform.processor()),
                ('Python版本', platform.python_version()),
                ('接入主机数量', Host.objects.count()),
                ('业务数量', Project.objects.count()),
                ('客户端运行情况', '运行中 %s,未运行 %s' % (upMinionCount, downMinionCount)),
            ),
            classes='table-bordered table-condensed '
                    'table-hover table-striped'
        )

        return [item_info]


class BoxMachineBasicInfoChart(Box):
    def get_items(self):
        item_chart = Item(
            html_id='machine-usage',
            name='主机资源',
            value=machine_usage_chart(),
            display=Item.AS_HIGHCHARTS)

        return [item_chart]


class BoxMinionStatusChart(Box):
    def get_items(self):
        item_chart = Item(
            html_id='minion-usage',
            name='操作系统分布',
            value=minion_status_chart(),
            display=Item.AS_HIGHCHARTS)

        return [item_chart]
