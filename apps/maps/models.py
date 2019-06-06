from datetime import datetime

from django.db import models
from django.contrib.auth.models import PermissionsMixin, Group


class CityDict(models.Model):
    """
    城市多级模型
    """

    CATEGORY_TYPE = (
        (1, '一级地区'),
        (2, '二级地区'),
        (3, '三级地区'),
    )
    name = models.CharField(default='', max_length=50, verbose_name='名称')
    desc = models.TextField(default='', verbose_name='地区描述')
    category_type = models.IntegerField(
        choices=CATEGORY_TYPE, verbose_name='地区级别')
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        verbose_name='父级类目',
        related_name='children')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '多级地区'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 自定义模型管理器 -- 暂时不用
class NewManager(models.Manager):
    def __init__(self, parent_category, *args, **kwargs):
        self.parent_category = parent_category
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(parent_category=self.parent_category)


class Map(models.Model):
    """
    地图资源模型
    """
    name = models.CharField(max_length=50, verbose_name='监控点名称')
    longitude = models.FloatField(blank=True, null=True, verbose_name='经度')
    latitude = models.FloatField(blank=True, null=True, verbose_name='纬度')
    dev_id = models.CharField(default='', unique=True, max_length=100, verbose_name='设备id')
    resource_id = models.CharField(default='', max_length=100, verbose_name='视频流id')
    status = models.IntegerField(default=1, verbose_name='设备状态')
    city = models.ForeignKey(CityDict,related_name='maps',default=1, on_delete=models.CASCADE,verbose_name='所属地区')
    address = models.CharField(max_length=100, default='苏州市平江路', verbose_name='地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '地图管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_sum_warn(self):
        """
        获取单个监控点所有预警事件　
        """
        return self.warnmodel_set.count()

    def get_make_warn(self):
        """
        获取未处理预警数
        """
        return self.warnmodel_set.filter(is_make=1).count()

