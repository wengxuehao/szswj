# __author__ : htzs
# __time__   : 19-4-2 上午11:18

from django.db.models.signals import post_save, post_delete
from django.contrib.auth import user_logged_in, user_logged_out
from django.dispatch import receiver

from apps.warnlist.models import WarnModel, WarnManage
from apps.users.models import User
from .user_log import get_user_log


def user_login_signal():
    @receiver(user_logged_in, sender=User)
    def my_callback(sender, **kwargs):
        print('请求登录测试信号。')


def user_logout_signal(request):
    @receiver(user_logged_out, sender=User)
    def my_callback(sender, **kwargs):
        print('请求登录测试信号。')


def warn_signal_save():
    @receiver(post_save, sender=WarnModel)
    def my_callback(sender, **kwargs):
        print('warn_signal_del')


def warn_signal_del():
    @receiver(post_delete, sender=WarnModel)
    def my_callback(sender, **kwargs):
        print('warn_signal_del')


def manage_signal_save():
    @receiver(post_save, sender=WarnManage)
    def my_callback(sender, **kwargs):
        print('请求测试信号。')


def manage_signal_del():
    @receiver(post_delete, sender=WarnManage)
    def my_callback(sender, **kwargs):
        print('请求测试信号。')