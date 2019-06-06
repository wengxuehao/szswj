# __author__ : htzs
# __time__   : 19-4-2 上午8:22


from apps.public.models import UserLog


def get_user_log(request, user_type, detail):
    """
    用户日志
    :param request:
    :param user_type:
    :return:
    """
    user_log = UserLog()
    user_log.user = request.user.username
    user_log.user_type = user_type
    user_log.ip_address = request.META['REMOTE_ADDR']
    user_log.desc = detail
    user_log.save()

