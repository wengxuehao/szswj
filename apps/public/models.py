from datetime import datetime
import time

from django.db import models

from apps.users.models import User


class UserLog(models.Model):
    """
    用户操作日志
    """
    MAKE_TYPE = ((1, '增加'), (2, '修改'), (3, '删除'), (4, '登陆'), (5, '退出'), (6, '查看'))
    user = models.CharField(max_length=50, verbose_name='操作用户')
    ip_address = models.CharField(default='', max_length=30, verbose_name='ip地址')
    user_type = models.IntegerField(choices=MAKE_TYPE, verbose_name='操作类型')
    desc = models.CharField(max_length=100, default='', verbose_name='操作详情')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='操作时间')

    class Meta:
        verbose_name = '用户操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.desc


class HwHttp(models.Model):
    """
    华为统计请求次数
    """
    HTTP_TYPE = ((1, '请求'), (2, '返回'))
    type = models.IntegerField(choices=HTTP_TYPE, verbose_name='方式')
    add_time = models.FloatField(default=1.0, verbose_name='请求时间')

    class Meta:
        verbose_name = '华为统计'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']


class ZwHttp1(models.Model):
    """
    中威统计请求次数
    """
    HTTP_TYPE = ((1, '请求'), (2, '返回'))
    type = models.IntegerField(choices=HTTP_TYPE, verbose_name='方式')
    add_time = models.FloatField(default=1.0, verbose_name='请求时间')

    class Meta:
        verbose_name = '中威统计'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']


class ZwHttp2(models.Model):
    """
    请求截图和视频统计
    """
    HTTP_TYPE = ((1, '图片'), (2, '视频'))
    CATE_TYPE = ((1, '请求'), (2, '返回'))
    category = models.IntegerField(choices=CATE_TYPE, verbose_name='类别')
    type = models.IntegerField(choices=HTTP_TYPE, verbose_name='方式')
    add_time = models.FloatField(default=1.0, verbose_name='请求时间')

    class Meta:
        verbose_name = '中威发送统计'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']
