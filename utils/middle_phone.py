import re

from django.http import HttpResponse


class MobileMiddleware(object):
    # 判断访问设备，手机端拦截
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        agent = request.META['HTTP_USER_AGENT'].lower()
        pattern = re.search('iphone', agent) or re.search('android', agent)
        if pattern:
            return HttpResponse('手机版暂未开发，请访问电脑版！')
        response = self.get_response(request)
        return response
