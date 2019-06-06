from django.http import HttpResponse, HttpResponseBadRequest
# from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
# from django.contrib.sessions.middleware import SessionMiddleware
# from django.middleware.common import CommonMiddleware
# from django.contrib.sessions.models import Session
# from django.contrib.sessions.backends import cache,cached_db
# from django.core.cache.backends.locmem import LocMemCache
# from django.core.signals import request_finished
# from django.core.signals import request_started
# from django.db.models.signals import pre_delete
#
#

# class AuthMiddleWare(MiddlewareMixin):
#     """
#     登录验证中间件
#     """
#
#     def process_request(self,request):
#         """
#         拦截请求　验证用户登录状态
#         """
#         if request.path == '/users/login/' or request.user.is_authenticated:
#             return None
#         else:
#             return HttpResponseRedirect('/users/login/')


class AuthMiddleWare(object):
    # 判断访问ip // 捕获异常
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            pass
        # except ConnectionResetError:
        except ConnectionResetError:
            return HttpResponseBadRequest()
        response = self.get_response(request)
        return response

