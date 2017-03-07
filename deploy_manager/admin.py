from django.contrib import admin
from deploy_manager.admins import *
from deploy_manager.models import *

admin.register(DeployJob, DeployJobAdmin)
admin.register(Project, ProjectAdmin)
admin.register(ProjectModule, ProjectModuleAdmin)
