from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser,Permission,PermissionsMixin,Group


class UserGroup(models.Model):
    """
    权限角色
    """
    group = models.OneToOneField(Group,on_delete=models.CASCADE,verbose_name='角色名')
    desc = models.CharField(max_length=100,default='',verbose_name='权限描述')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name = '权限角色'
        verbose_name_plural = verbose_name
    
    @property
    def get_group_name(self):
        return self.group.name,self.group.id


class User(AbstractUser):
    """
    用户模型
    """
    telephone = models.CharField(max_length=11, default='', verbose_name='手机号')

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


