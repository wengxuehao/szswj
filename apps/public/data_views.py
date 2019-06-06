# __author__ : htzs
# __time__   : 19-5-29 下午1:00

import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q

from apps.maps.models import Map
from apps.warnlist.models import WarnModel
from apps.public.models import HwHttp, ZwHttp1, ZwHttp2

from utils import restful


class TopFiveView(View):
    """
    返回top5预警数据
    """

    def get(self, request):
        try:
            warn_sum = Map.objects.all()
        except Exception as e:
            return restful.params_error(message=e)
            pass
        else:
            warn_list = []
            for map in warn_sum:
                data = {'value': map.get_sum_warn(), 'name': map.name}
                warn_list.append(data)
            data = sorted(
                warn_list, key=lambda x: x['value'], reverse=True)[:5]
            return restful.result(data=data)


class TopThreeView(View):
    """
    返回top3预警数据
    """

    def get(self, request):
        try:
            warn_sum = Map.objects.all()
        except Exception as e:
            return restful.params_error(message=e)
            pass
        else:
            warn_list = []
            for map in warn_sum:
                data = {'value': map.get_sum_warn(), 'name': map.name}
                warn_list.append(data)
            data = sorted(
                warn_list, key=lambda x: x['value'], reverse=True)[:3]
            return restful.result(data=data)


class WarnTypeView(View):
    """
    返回智能与手动预警对比数据
    """

    def get(self, request):
        try:
            warn_z = WarnModel.objects.filter(warn_type=1).count()
            warn_s = WarnModel.objects.filter(warn_type=2).count()
        except Exception as e:
            return restful.params_error(message=e)
        else:
            if warn_z >= warn_s:
                name = '智能预警'
            else:
                name = '手动预警'
            data = {
                'sum_data': [{
                    'value': warn_z,
                    'name': '智能预警'
                }, {
                    'value': warn_s,
                    'name': '手动预警'
                }],
                'count': warn_z + warn_s,
                'name': name
            }
            return restful.result(data=data)


class CakeDataView(View):
    """
    蛋糕图统计
    """

    def get(self, request):
        # 1天数据 - 每隔6小时统计一次
        today = datetime.date.today()
        today_data = WarnModel.objects.filter(add_time__gte=today).values(
            'warn_manage', 'add_time')
        data_list1 = []
        data_list2 = []
        data1 = today_data.filter(warn_manage=9)
        data2 = today_data.filter(warn_manage=10)

        time_list = [4, 9, 14, 19, 24]
        for i in time_list:
            select_data1 = data1.filter(add_time__hour__range=(i,
                                                               i + 5)).count()
            select_data2 = data2.filter(add_time__hour__range=(i,
                                                               i + 5)).count()
            data_list1.append(select_data1)
            data_list2.append(select_data2)
        data = {'Spilling': data_list1, 'water': data_list2}
        return restful.result(data=data)


class LineDataView(View):
    """
    左下柱状图数据
    """

    def get(self, request):
        index = request.GET.get('index', 0)
        index = int(index)
        if index == 0:
            # 24小时数据 每隔2小时统计一次
            today = datetime.date.today()
            now_warn = WarnModel.objects.filter(add_time__gte=today).values(
                'is_make', 'add_time').exclude(is_make__in=[1, 2])
            data_list = []
            data1 = now_warn.filter(is_make=3)
            data2 = now_warn.filter(Q(is_make=4) | Q(is_make=5))
            for i in range(0, 23):
                if i % 2 == 0:
                    filter_data1 = data1.filter(
                        Q(add_time__hour=i) | Q(add_time__hour=i + 1)).count()
                    filter_data2 = data2.filter(
                        Q(add_time__hour=i) | Q(add_time__hour=i + 1)).count()
                    data = {
                        'product': f'{i}点',
                        '已完成': filter_data1,
                        '已丢弃': filter_data2
                    }
                    data_list.append(data)
            return restful.result(data=data_list)

        elif index == 1:
            # 近七天数据
            now_week = datetime.datetime.now().isocalendar()[1]
            filter_data = WarnModel.objects.filter(
                add_time__week=now_week).values(
                'is_make', 'add_time').exclude(is_make__in=[1, 2])
            data_list = []
            data1 = filter_data.filter(is_make=3)
            data2 = filter_data.filter(Q(is_make=4) | Q(is_make=5))
            for i in range(2, 8):
                filter_data1 = data1.filter(add_time__week_day=i).count()
                filter_data2 = data2.filter(add_time__week_day=i).count()
                num_list = ['一', '二', '三', '四', '五', '六', '日']
                data = {
                    'product': f'周{num_list[i-2]}',
                    '已完成': filter_data1,
                    '已丢弃': filter_data2
                }
                data_list.append(data)
            filter_data1 = data1.filter(add_time__week_day=1).count()
            filter_data2 = data2.filter(add_time__week_day=1).count()
            data = {'product': '周日', '已完成': filter_data1, '已丢弃': filter_data2}
            data_list.append(data)
            return restful.result(data=data_list)

        elif index == 2:
            # 按月统计
            month_data = WarnModel.objects.values(
                'is_make', 'add_time').exclude(is_make__in=[1, 2])
            data_list = []
            data1 = month_data.filter(is_make=3)
            data2 = month_data.filter(Q(is_make=4) | Q(is_make=5))
            for i in range(1, 13):
                filter_data1 = data1.filter(add_time__month=i).count()
                filter_data2 = data2.filter(add_time__month=i).count()
                data = {
                    'product': f'{i}月',
                    '已完成': filter_data1,
                    '已丢弃': filter_data2
                }
                data_list.append(data)
            return restful.result(data=data_list)
        return restful.result()


class ColumnDataView(View):
    """
    柱状图统计
    """

    def get(self, request):
        index = request.GET.get('index', 0)
        index = int(index)
        if index == 0:
            # 24小时数据 每隔2小时统计一次
            today = datetime.date.today()
            now_warn = WarnModel.objects.filter(add_time__gte=today).values(
                'warn_manage', 'add_time')
            data_list = []
            data1 = now_warn.filter(warn_manage=9)
            data2 = now_warn.filter(warn_manage=10)
            for i in range(0, 23):
                if i % 2 == 0:
                    filter_data1 = data1.filter(
                        Q(add_time__hour=i) | Q(add_time__hour=i + 1)).count()
                    filter_data2 = data2.filter(
                        Q(add_time__hour=i) | Q(add_time__hour=i + 1)).count()
                    data = {
                        'product': f'{i}点',
                        '抛物预警': filter_data1,
                        '泼水预警': filter_data2
                    }
                    data_list.append(data)
            return restful.result(data=data_list)

        elif index == 1:
            # 近七天数据
            now_week = datetime.datetime.now().isocalendar()[1]
            filter_data = WarnModel.objects.filter(
                add_time__week=now_week).values('warn_manage', 'add_time')
            data_list = []
            data1 = filter_data.filter(warn_manage=9)
            data2 = filter_data.filter(warn_manage=10)
            for i in range(2, 8):
                filter_data1 = data1.filter(add_time__week_day=i).count()
                filter_data2 = data2.filter(add_time__week_day=i).count()
                num_list = ['一', '二', '三', '四', '五', '六', '日']
                data = {
                    'product': f'周{num_list[i-2]}',
                    '抛物预警': filter_data1,
                    '泼水预警': filter_data2
                }
                data_list.append(data)
            filter_data1 = data1.filter(add_time__week_day=1).count()
            filter_data2 = data2.filter(add_time__week_day=1).count()
            data = {
                'product': '周日',
                '抛物预警': filter_data1,
                '泼水预警': filter_data2
            }
            data_list.append(data)
            return restful.result(data=data_list)

        elif index == 2:
            # 按月统计
            month_data = WarnModel.objects.values('warn_manage', 'add_time')
            data_list = []
            data1 = month_data.filter(warn_manage=9)
            data2 = month_data.filter(warn_manage=10)
            for i in range(1, 13):
                filter_data1 = data1.filter(add_time__month=i).count()
                filter_data2 = data2.filter(add_time__month=i).count()
                data = {
                    'product': f'{i}月',
                    '抛物预警': filter_data1,
                    '泼水预警': filter_data2
                }
                data_list.append(data)
            return restful.result(data=data_list)
        return restful.result()


class HttpDataView(View):
    """
    返回数据
    """

    def get(self, request):
        try:
            type = request.GET.get('type', '1')
        except:
            return restful.params_error(message='参数有误.')
        type = int(type)
        try:
            if type == 1:
                http_request = HwHttp.objects.filter(type=1).count()
                http_response = HwHttp.objects.filter(type=2).count()
                stop_time = HwHttp.objects.all().first().add_time
                start_time = HwHttp.objects.all().last().add_time
                data = {
                    '华为预警请求': http_request,
                    '平台响应': http_response,
                    '统计开始时间': start_time,
                    '统计结束时间': stop_time
                }
                return restful.result(data=data, message='success')
            elif type == 2:
                http_rec_request = ZwHttp1.objects.filter(type=1).count()
                http_rec_response = ZwHttp1.objects.filter(type=2).count()
                stop_time = ZwHttp1.objects.all().first().add_time
                start_time = ZwHttp1.objects.all().last().add_time
                data_1 = {
                    '接收中威响应': http_rec_request,
                    '平台响应': http_rec_response,
                    '统计开始时间': start_time,
                    '统计结束时间': stop_time
                }
                http_pic_request = ZwHttp2.objects.filter(
                    Q(category=1) & Q(type=1)).count()
                http_pic_response = ZwHttp2.objects.filter(
                    Q(category=1) & Q(type=2)).count()
                http_video_request = ZwHttp2.objects.filter(
                    Q(category=2) & Q(type=1)).count()
                http_video_response = ZwHttp2.objects.filter(
                    Q(category=2) & Q(type=2)).count()
                stop_time = ZwHttp2.objects.all().first().add_time
                start_time = ZwHttp2.objects.all().last().add_time
                data_2 = {
                    '截图请求': http_pic_request,
                    '截图响应': http_pic_response,
                    '视频请求': http_video_request,
                    '视频响应': http_video_response,
                    '统计开始时间': start_time,
                    '统计结束时间': stop_time
                }

                data = {'中威请求平台': data_1, '平台请求截图/视频': data_2}

                return restful.result(data=data, message='success')
        except:
            return restful.result(message='type参数仅为1和2')
        return restful.result(message='type参数仅为1和2')


class IndexDataView(View):
    """
    数据大屏 -- 各种统计数据
    """

    def _data(self, rec_data, send_data, num):
        data1 = 0
        try:
            data_1 = '%.2f%%' % (rec_data / send_data)

        except ZeroDivisionError:
            data_1 = '0.00%'
        else:
            data1 = int(eval(data_1.strip('%')))
        context = {
            'data_{0}'.format(num): data_1,
            'data{0}'.format(num): data1,
        }
        return context

    def get(self, request):
        # 城管 -- 回复率
        now_week = datetime.datetime.now().isocalendar()[1]
        warns = WarnModel.objects.filter(add_time__week=now_week)

        rec_data1 = warns.filter(Q(is_make=3) | Q(is_make=4)).count()
        send_data1 = warns.filter(~(Q(is_make=1) | Q(is_make=5))).count()

        context1 = self._data(rec_data1, send_data1, 1)

        # 城管 -- 完结率
        rec_data2 = warns.filter(is_make=3).count()
        send_data2 = send_data1
        context2 = self._data(rec_data2, send_data2, 2)
        context1.update(context2)

        # 城管 -- 丢弃率
        rec_data3 = warns.filter(is_make=4).count()
        send_data3 = send_data1
        context3 = self._data(rec_data3, send_data3, 3)
        context1.update(context3)

        # 系统 -- 处理率
        rec_data4 = warns.exclude(is_make=1).count()
        send_data4 = warns.count()
        context4 = self._data(rec_data4, send_data4, 4)
        context1.update(context4)

        # 系统 -- 上报率
        send_data5 = warns.count()
        rec_data5 = send_data1
        context5 = self._data(rec_data5, send_data5, 5)
        context1.update(context5)

        # 系统 -- 丢弃率
        send_data6 = warns.count()
        rec_data6 = warns.filter(is_make=5).count()
        context6 = self._data(rec_data6, send_data6, 6)
        context1.update(context6)

        # 待办预警
        today = datetime.date.today()
        today_data = warns.filter(add_time__gte=today)
        today_rec = today_data.filter(is_make=1).count()

        # 今日预警总量
        today_all = today_data.count()

        # 预警丢弃
        today_del = today_data.filter(is_make=5).count()

        # 上报城管
        today_send = today_data.filter(Q(is_make=2) | Q(is_make=3) | Q(is_make=4)).count()

        # 城管办理
        today_make = today_data.filter(is_make=3).count()

        # 城管反馈
        today_sum = today_data.filter(Q(is_make=3) | Q(is_make=4)).count()

        # 监控总数
        map_all = Map.objects.all().count()

        # 在线监控数
        map_online = Map.objects.filter(status=1).count()

        # 离线监控数
        map_fail = Map.objects.filter(status=0).count()

        # 最新预警
        new_warns = warns.values('event_id', 'add_time', 'map__name')[:4]

        sum_data = {
            'today_rec': today_rec,
            'today_send': today_send,
            'today_del': today_del,
            'today_make': today_make,
            'today_sum': today_sum,
            'today_all': today_all,
            'map_all': map_all,
            'map_online': map_online,
            'map_fail': map_fail,
            'new_warns': new_warns
        }
        context1.update(sum_data)

        return render(request, 'users/index-data.html', context=context1)

