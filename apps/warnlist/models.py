from datetime import datetime

from django.db import models

from apps.maps.models import Map
from apps.users.models import User


class WarnType(models.Model):
    """
    预警分析类型模型
    """
    TYPE_CHOICES = (('other', '其他检测'), ('splashing', '泼水检测'), ('throwing', '抛物检测'))
    type_id = models.CharField(max_length=100, verbose_name='检测类型id')
    type_name = models.CharField(choices=TYPE_CHOICES, max_length=100, verbose_name='检测类型名')
    desc = models.CharField(default='', max_length=100, verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '预警分析类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type_name


class StreamId(models.Model):
    stream_id = models.CharField(max_length=100, verbose_name='创建的视频流id')
    resource_id = models.CharField(default='', max_length=100, verbose_name='设备视频流id')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频流id模型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.stream_id


class WarnManage(models.Model):
    """
    设备预警分析任务模型
    """
    type = models.ForeignKey(WarnType, on_delete=models.CASCADE, verbose_name='所属预警分析类型')
    map = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name='所属设备')
    process_id = models.CharField(max_length=50, default='', verbose_name='任务编号')
    stream = models.ForeignKey(StreamId, on_delete=models.CASCADE, verbose_name='所属视频流id')
    type_name = models.CharField(max_length=100, verbose_name='检测类型名')
    desc = models.CharField(default='', max_length=100, verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '设备预警分析任务'
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    def __str__(self):
        return self.type_name


class WarnModel(models.Model):
    """
    预警事件模型
    """
    MAKE_CHOICES = ((1, '待处理'), (2, '已发送'), (3, '已完成'), (4, '城管已丢弃'), (5, '平台已丢弃'))
    TYPE_CHOICES = ((1, '智能预警'), (2, '手动预警'))
    DAYS_CHOICES = ((0, '夜晚'), (1, '白天'), (2, '手动'))
    event_id = models.CharField(default='', max_length=100,verbose_name='预警编号')
    map = models.ForeignKey(Map, on_delete=models.CASCADE, verbose_name='所属监控点')
    warn_manage = models.ForeignKey(WarnType, on_delete=models.CASCADE, verbose_name='所属任务类型')
    user = models.CharField(max_length=50, default='', verbose_name='平台处理人员')
    manage_user = models.CharField(max_length=50, default='', verbose_name='城管处理人员')
    warn_type = models.IntegerField(default=1, choices=TYPE_CHOICES, verbose_name='预警类型')
    is_day = models.IntegerField(default=1, choices=DAYS_CHOICES, verbose_name='白天黑夜')
    start_time = models.BigIntegerField(default=1, verbose_name='预警开始时间')
    end_time = models.BigIntegerField(default=1, verbose_name='预警结束时间')
    video_url = models.CharField(max_length=300, default='', db_index=True, verbose_name='违法视频')
    warn_url = models.CharField(max_length=300, default='', db_index=True, verbose_name='标注图片')
    image_sign = models.CharField(max_length=50, default='', db_index=True, verbose_name='标注参数')
    is_make = models.IntegerField(default=1, choices=MAKE_CHOICES, db_index=True, verbose_name='预警状态')
    result = models.CharField(max_length=300, default='处理中', db_index=True, verbose_name='处理进度')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '预警数据管理'
        verbose_name_plural = verbose_name
        ordering = ('-add_time',)

    def rec_image(self):
        """
        获取预警图片
        :return:
        """
        all_image = self.images.all()
        return all_image

    def __str__(self):
        return self.event_id


class WarnImage(models.Model):
    """
    预警图片模型
    """
    title = models.CharField(default='预警图片',max_length=50, verbose_name='图片名称')
    image_url = models.CharField(max_length=300, db_index=True, verbose_name='图片地址')
    warn_image = models.ForeignKey(WarnModel, related_name='images', on_delete=models.CASCADE, verbose_name='所属预警')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '预警图片管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class ManageImage(models.Model):
    """
    城管图片模型
    """
    images_url = models.CharField(max_length=300, db_index=True, verbose_name='图片地址')
    manage_image = models.ForeignKey(WarnModel, related_name='manage_images', on_delete=models.CASCADE, verbose_name='所属预警')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '城管图片管理'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return self.id


class NewWarn(models.Model):
    """
    首页预警数据
    """
    name = models.CharField(max_length=50, verbose_name='设备名称')
    event_id = models.CharField(default='', max_length=100, verbose_name='预警编号')
    image_url = models.CharField(max_length=300, db_index=True, verbose_name='图片地址')
    image_sign = models.CharField(max_length=100, default='', verbose_name='标注信息')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        ordering = ('-add_time',)
        verbose_name = '首页预警数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 分表代码
# class TableModel(models.Model):
#     @classmethod
#     def filter_table(cls, dataid):
#         slice = int(dataid / 10)
#         if slice == 0:
#             db_name = 'demo_point'
#         else:
#             db_name = 'demo_point{}'.format(slice)
#         cls._meta.db_table = db_name
#         return cls.objects.filter(dataid=dataid)
#
#     def save(self, force_insert=False, force_update=False, using=None,
#              update_fields=None):
#         slice = int(self.dataid / 10)
#         if slice == 0:
#             db_name = 'demo_point'
#         else:
#             db_name = 'demo_point{}'.format(slice)
#         self._meta.db_table = db_name
#         super().save()
