from django.shortcuts import render
from rest_framework import viewsets

from deploy_manager.models import *
from deploy_manager.serializers import *


class ProjectVersionViewSet(viewsets.ModelViewSet):
    queryset = ProjectVersion.objects.all()
    serializer_class = ProjectVersionSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DeployJobViewSet(viewsets.ModelViewSet):
    queryset = DeployJob.objects.all()
    serializer_class = DeployJobSerializer

