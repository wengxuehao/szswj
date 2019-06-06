from rest_framework import serializers
from .models import Play, Video


class PlaySerializers(serializers.ModelSerializer):
    """
    直播视频流序列化
    """
    class Meta:
        model = Play
        fields = ('id', 'map', 'video', 'monitor_id', 'add_time')


class VideoSerializers(serializers.ModelSerializer):
    """
    视频录像序列化
    """
    class Meta:
        model = Video
        fields = ('id', 'map', 'video', 'monitor_id', 'add_time')