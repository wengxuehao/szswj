from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from apps.users.models import User
from apps.maps.models import Map
from apps.video.models import Play, Video
from apps.warnlist.models import WarnManage, WarnModel, WarnType
from apps.public.models import UserLog
from utils import restful


# ××××××××××××××××× 权限分配函数 ×××××××××××××××××
def view_index():
    # 控制台
    content_type = ContentType.objects.get_for_model(Map)
    permission_map = Permission.objects.get(
        codename='view_map', content_type=content_type)
    return permission_map


def view_video():
    # 视频监控
    content_type = ContentType.objects.get_for_model(Video)
    permission_video = Permission.objects.get(
        codename='view_video', content_type=content_type)
    return permission_video


def view_map():
    # 视频墙页
    content_type = ContentType.objects.get_for_model(Video)
    permission_make_video = Permission.objects.get(
        codename='change_video', content_type=content_type)
    return permission_make_video


def view_play():
    # 录像查看
    content_type = ContentType.objects.get_for_model(Play)
    permission_play = Permission.objects.get(
        codename='view_play', content_type=content_type)
    return permission_play


def view_warn():
    # 预警分析
    content_type = ContentType.objects.get_for_model(WarnModel)
    permission_warn = Permission.objects.get(
        codename='view_warnmodel', content_type=content_type)
    return permission_warn


def view_sum():
    # 统计备案
    content_type = ContentType.objects.get_for_model(WarnType)
    permission_sum = Permission.objects.get(
        codename='view_warntype', content_type=content_type)
    return permission_sum


def make_video():
    # 监控管理
    content_type = ContentType.objects.get_for_model(Play)
    permission_make_warn = Permission.objects.get(
        codename='change_play', content_type=content_type)
    return permission_make_warn


def warn_manage():
    # 任务管理
    content_type = ContentType.objects.get_for_model(WarnManage)
    permission_warn_manage = Permission.objects.get(
        codename='view_warnmanage', content_type=content_type)
    return permission_warn_manage


def make_user():
    # 用户管理
    content_type = ContentType.objects.get_for_model(User)
    permission_make_play = Permission.objects.get(
        codename='view_user', content_type=content_type)
    return permission_make_play


def manage_log():
    # 操作日志
    content_type = ContentType.objects.get_for_model(UserLog)
    permission_manage_log = Permission.objects.get(
        codename='view_userlog', content_type=content_type)
    return permission_manage_log


def user_perms():
    """
    用户权限筛选
    """
    perm_data = [
    {
        'value': 1,
        'title': '控制台',
        'data': view_index()
    }, {
        'value': 2,
        'title': '视频监控',
        'data': view_video()
    }, {
        'value': 3,
        'title': '视频墙页',
        'data': view_map()
    }, {
        'value': 4,
        'title': '录像查看',
        'data': view_play()
    }, {
        'value': 5,
        'title': '预警分析',
        'data': view_warn()
    }, {
        'value': 6,
        'title': '统计备案',
        'data': view_sum()
    }, {
        'value': 7,
        'title': '监控管理',
        'data': make_video()
    }, {
        'value': 8,
        'title': '任务管理',
        'data': warn_manage()
    }, {
        'value': 9,
        'title': '用户管理',
        'data': make_user()
    }, {
        'value': 10,
        'title': '操作日志',
        'data': manage_log()
    }]
    return perm_data


def add_manage(check_val):
    user_perm = user_perms()
    perm_list = []
    try:
        if isinstance(check_val, list):
            for i in check_val:
                perm_list.append(user_perm[i-1]['data'])
            return perm_list
        elif isinstance(check_val, int):
            perm_list.append(user_perm[check_val-1]['data'])
            return perm_list
    except Exception as e:
        return restful.params_error(message=e)


def auth_perm(user):
    perm_data = {
        'maps.view_map': 'index',  # 控制台
        'video.view_video': 'video:video',  # 视频监控
        'video.change_video': 'video:video_home',  # 视频墙页
        'video.view_play': 'video:view_video',  # 录像查看
        'video.change_play': 'video:video_manage',   # 监控管理
        'warnlist.view_warnmodel': 'warnlist:warn_list',  # 预警分析
        'warnlist.view_warntype': 'warnlist:sum_list',  # 统计备案
        'warnlist.view_warnmanage': 'warnlist:warn_manage',  # 任务管理
        'users.view_user': 'users:user_manage',  # 用户管理
        'public.view_userlog': 'public:log',  # 操作日志
    }
    perm_keys = ['maps.view_map', 'video.view_video', 'video.change_video', 'video.view_play', 'video.change_play',
                 'warnlist.view_warnmodel', 'warnlist.view_warntype', 'warnlist.view_warnmanage',
                 'users.view_user', 'public.view_userlog']
    all_perm = user.get_all_permissions()
    for index, i in enumerate(perm_keys):
        if perm_keys[index] in list(all_perm):
            if perm_keys[0] in list(all_perm):
                return perm_data[perm_keys[0]]
            perm_url = perm_data[perm_keys[index]]
            return perm_url
        else:
            continue

