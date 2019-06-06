from datetime import datetime

from django.db import models

from apps.maps.models import Map



class Play(models.Model):
    """
    播放视频模型
    """
    map = models.OneToOneField(Map, on_delete=models.DO_NOTHING, verbose_name='所属设备')
    video = models.CharField(max_length=1000, default='', verbose_name='监控直播地址')
    monitor_id = models.CharField(max_length=100, verbose_name='播放直播流id')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '播放视频管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.monitor_id


class Video(models.Model):
    """
    播放录像模型
    """
    map = models.OneToOneField(Map, on_delete=models.DO_NOTHING, verbose_name='所属设备')
    video = models.CharField(max_length=1000, default='', verbose_name='监控录像地址')
    monitor_id = models.CharField(max_length=100, verbose_name='播放录像id')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '播放录像管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.monitor_id