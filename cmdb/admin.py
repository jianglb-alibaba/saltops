import requests
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import redirect
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from cmdb.admins import *
from cmdb.models import *
from deploy_manager.models import *
from saltjob.salt_https_api import salt_api_token
from saltjob.salt_token_id import token_id
from saltjob.tasks import scanHostJob
from saltops.settings import SALT_CONN_TYPE, SALT_HTTP_URL, SALT_REST_URL

admin.register(Host, HostAdmin)
admin.register(Cabinet, CabinetAdmin)
admin.register(IDCLevel, IDCLevelAdmin)
admin.register(ISP, ISPAdmin)
admin.register(IDC, IDCAdmin)
admin.register(Rack, RackAdmin)
