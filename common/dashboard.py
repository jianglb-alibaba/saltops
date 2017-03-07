from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard

from common.dashboard_modules import OverView, HostResourceOverView, HostTypeOverView


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(OverView())
        self.children.append(HostResourceOverView())
        self.children.append(HostTypeOverView())