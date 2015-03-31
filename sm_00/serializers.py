from django.contrib.auth.models import User
from django.forms import widgets

from rest_framework import serializers

from slave.models import Slave
from task.models import Task, Assignment

class UserSerializer(serializers.ModelSerializer):
    slaves = serializers.PrimaryKeyRelatedField(many=True, queryset=Slave.objects.all())
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'slaves', 'tasks')
