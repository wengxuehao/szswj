#!/home/htzs/mydjango/bin/python3
# -*- encoding: utf-8 -*-
'''
@File    :   serializers.py
@Time    :   2019/02/26 14:20:47
@Author  :   adminy 
@Version :   1.0
@Contact :   www.htzs@qq.com
'''

from rest_framework import serializers
from .models import WarnModel, WarnImage, WarnManage, WarnType, NewWarn, ManageImage


class WarnImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = WarnImage
        fields = ('image_url',)


class ManageImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = ManageImage
        fields = ('images_url',)


class WarnSerializers(serializers.ModelSerializer):
    """
    预警模型序列化
    """
    is_make = serializers.CharField(source='get_is_make_display')
    warn_type = serializers.CharField(source='get_warn_type_display')
    map_name = serializers.CharField(source='map.name')
    dev_id = serializers.CharField(source='map.dev_id')
    type_name = serializers.CharField(source='warn_manage.desc')
    images = WarnImageSerializers(many=True, read_only=True)
    add_time = serializers.DateTimeField(format="%m/%d %H:%M:%S", required=False, read_only=True)
    # add_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = WarnModel
        fields = ['id', 'event_id', 'user', 'warn_url', 'image_sign', 'images', 'type_name', 'map_name', 'video_url',
                  'dev_id', 'warn_type', 'is_make', 'manage_user', 'result', 'add_time']


class ManageWarnSerializers(serializers.ModelSerializer):
    """
    预警模型序列化
    """
    is_make = serializers.CharField(source='get_is_make_display')
    warn_type = serializers.CharField(source='get_warn_type_display')
    map_name = serializers.CharField(source='map.name')
    type_name = serializers.CharField(source='warn_manage.desc')
    images = WarnImageSerializers(many=True, read_only=True)
    manage_images = ManageImageSerializers(many=True, read_only=True)
    add_time = serializers.DateTimeField(format="%m/%d %H:%M:%S", required=False, read_only=True)

    # add_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = WarnModel
        fields = ['id', 'event_id', 'user', 'manage_user', 'warn_url', 'image_sign', 'images', 'manage_images', 'type_name',
                  'map_name', 'video_url', 'result', 'warn_type', 'is_make', 'add_time']


class NewWarnSerializers(serializers.ModelSerializer):
    """
    首页预警序列化
    """
    add_time = serializers.DateTimeField(format="%m/%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = NewWarn
        fields = ('id', "name", "event_id", "image_url", "add_time")


class IndexWarnSerializers(serializers.ModelSerializer):
    """
    首页预警图片序列化
    """

    class Meta:
        model = NewWarn
        fields = ("image_sign", "image_url")


class WarnTypeSerializers(serializers.ModelSerializer):
    """
    任务模型序列化
    """
    type_name = serializers.CharField(source='get_type_name_display')

    class Meta:
        model = WarnType
        fields = ('type_id', 'type_name')


class WarnProcessSerializers(serializers.ModelSerializer):
    """
    分析任务模型序列化
    """
    dev_id = serializers.CharField(source='map.dev_id')
    name = serializers.CharField(source='map.name')
    add_time = serializers.DateTimeField(format="%Y%m/%d %H:%M", required=False, read_only=True)

    class Meta:
        model = WarnManage
        fields = ("process_id", 'name', "dev_id", "type_name", "add_time")
