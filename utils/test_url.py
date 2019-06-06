# __author__ : htzs
# __time__   : 19-5-9 上午10:06


from django.core.cache import cache


def request_count():
    if cache.get('test_request'):
        cache.incr('test_request')
    else:
        cache.set('test_request', 0, 20000)
