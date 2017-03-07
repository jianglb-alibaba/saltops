# -*- coding: utf-8 -*-
"""saltops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import sys
sys.path.append("..")

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework import routers

# from deploy_manager.serializer import UserViewSet

from  dashboard.sites import DashboardSite

from deploy_manager.views import *
from saltops import settings


router = routers.DefaultRouter()
router.register(r'projectversionViewSet', ProjectVersionViewSet)
router.register(r'projectViewSet', ProjectViewSet)
router.register(r'deployJobViewSet', DeployJobViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^searchableselect/', include('searchableselect.urls')),
]

# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
admin.site.site_header = 'SaltOps'
admin.site.site_title = 'SaltOps'
