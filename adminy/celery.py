# # __author__ : htzs
# # __time__   : 19-4-16 上午8:58
#
# from __future__ import absolute_import
# import os
# from celery import Celery
# from django.conf import settings
#
#
# # 设置环境变量
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminy.settings')
#
# # 注册Celery的APP
# app = Celery('adminy')
#
# # 绑定配置文件
# app.config_from_object('django.conf:settings')
#
# # 自动发现各个app下的tasks.py文件
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) # 自动搜索
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))  # 打印本身 request 信息的任务
#
# # 启动
# # celery -A adminy worker -l info
#
# # 启动监控
# # python manage.py celery flower


# ****************** celery配置 ******************

# import djcelery
#
# djcelery.setup_loader()
#
# BROKER_BACKEND = 'redis'
#
# BROKER_URL = 'redis://localhost:6379/1'
#
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
#
# CELERY_TIMEZONE = "Asia/Shanghai"  # 指定时区，不指定默认为 'UTC'
#
# # 有些情况可以防止死锁
# CELERYD_FORCE_EXECV = True
#
# # 设置并发的worker数量
# CELERYD_CONCURRENCY = 4
#
# # 允许重试
# CELERY_ACKS_LATE = True
#
# # 每个worker最多执行100个任务被销毁，可以防止内存泄露
# CELERYD_MAX_TASKS_PER_CHILD = 100
#
# # 单个任务的最大运行时间
# CELERYD_TASK_TIME_LIMIT = 12 * 30
#
# CELERY_QUEUES = {
#     'work_queue': {
#         'exchange': 'work_queue',
#         'exchange_type': 'direct',
#         'binding_key': 'work_queue'
#     }
# }
#
# CELERY_DEFAULT_QUEUE = 'work_queue'
#
# CELERY_IMPORTS = (
#     'warnlist.tasks',
# )