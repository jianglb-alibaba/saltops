from django.contrib import admin
from tools_manager.admins import *
from tools_manager.models import *

admin.register(ToolsExecJob, ToolsExecJobAdmin)
admin.register(ToolsScript, ToolsScriptAdmin)
admin.register(ToolsTypes, ToolsTypesAdmin)
