from rest_framework import serializers

from deploy_manager.models import *
from saltjob.tasks import deployTask


class ProjectVersionSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        if validated_data['is_default'] == True:
            ProjectVersion.objects.filter(project=validated_data['project']).update(is_default=False)
        obj = ProjectVersion.objects.create(**validated_data)
        return obj

    class Meta:
        model = ProjectVersion
        fields = ('name', 'project', 'files', 'is_default')


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('name',)


class DeployJobSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        obj = DeployJob.objects.create(**validated_data)
        deployTask(obj)
        return obj

    class Meta:
        model = DeployJob
        fields = ('project_version', 'job_name')
