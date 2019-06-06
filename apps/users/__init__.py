# from django.core.signals import request_finished
# from django.dispatch import receiver


# # 方法一：装饰器模式
# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     print('请求测试信号。')

# *************************************8

# 方法二：调用函数connect模式
# request_started.connect(my_callback)