from random import Random
from contextlib import contextmanager

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import View as _View
from utils import restful


class UserAuthMixin(LoginRequiredMixin, PermissionRequiredMixin):
    pass
    # def dispatch(self, request, *args, **kwargs):
    #     if not self.has_permission():
    #         return restful.params_error(message='没有权限访问!')
    #     return super().dispatch(request, *args, **kwargs)


def random_str(random_length=10):
    """
    生成随机数
    :param random_length:
    :return:
    """
    random_list = []

    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        result = chars[random.randint(0, length)]
        random_list.append(result)
    randomld = ''.join(random_list)
    return randomld


@contextmanager
def make_error():
    try:
        yield
        return restful.result()
    except Exception as e:
        return restful.params_error(e)


class View(_View):
    with make_error():
        def dispatch(self, request, *args, **kwargs):
            super().dispatch(request, *args, **kwargs)
