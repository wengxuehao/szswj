from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User,UserGroup


# 系统角色模型序列化
class GroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Group
        fields = ('id', 'name')


# 用户角色模型序列化
class UserGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name')  # 获取外键字段
    add_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M", required=False, read_only=True)

    class Meta:
        model = UserGroup
        fields = ('id','desc','group_name','add_time')


# 用户模型序列化
class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(format="%Y/%m/%d %H:%M", required=False, read_only=True)
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'groups', 'password', 'email', 'date_joined')
