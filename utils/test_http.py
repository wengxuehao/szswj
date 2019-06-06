# __author__ : htzs
# __time__   : 19-5-14 上午11:41


import time

from django.core.cache import cache


class HttpTest:
    """
    设置缓存统计http
    """
    def __init__(self):
        self.time = time.time()
        self.sum_time = 60*60*24*7

    def set_cache(self):
        # cache.set('hw_time', self.time, self.sum_time)
        # cache.set('hw_request', 1, self.sum_time)
        # cache.set('hw_response', 1, self.sum_time)
        # cache.set('zw_request', 1, self.sum_time)
        # cache.set('zw_response', 1, self.sum_time)
        cache.delete('hw_time')
        cache.delete('hw_request')
        cache.delete('hw_response')
        cache.delete('zw_request')
        cache.delete('zw_response')
        return 'ok'

    def hw_http_request(self, rec_data):
        cache.incr('hw_request')

    def hw_http_response(self, rec_data):
        cache.incr('hw_response')

    def zw_http_request(self, rec_data):
        cache.incr('zw_request')

    def zw_http_response(self, rec_data):
        cache.incr('zw_response')
