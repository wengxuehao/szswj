import json
import time
import datetime

import requests
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from django.core.cache import cache

from apps.maps.models import Map, CityDict
from apps.warnlist.models import WarnType, WarnModel, WarnImage, NewWarn, ManageImage
from utils.clouds.ob_video import RecImage
from apps.maps.serializers import CityDictSerializers, BdMapSerializers
from apps.warnlist.serializers import NewWarnSerializers, IndexWarnSerializers
from rest_framework.renderers import JSONRenderer
from utils import restful, mixin
from utils.page_func import rec_page
from .serializers import UserLogSerializers
from .models import UserLog, HwHttp, ZwHttp1, ZwHttp2
from utils.mixin import UserAuthMixin
from apps.maps.serializers import MapSelectSerializers


class IndexView(UserAuthMixin, View):
    """
    首页
    """
    permission_required = 'maps.view_map'

    def get(self, request):
        """
        返回一些统计数据
        :param request:
        :return:
        """
        warn_count = WarnModel.objects.all().count()
        warn_success = WarnModel.objects.filter(is_make=3).count()
        warn_delete = WarnModel.objects.filter(Q(is_make=4) | Q(is_make=5)).count()
        context = {
            'warn_count': warn_count,
            'warn_success': warn_success,
            'warn_delete': warn_delete
        }
        return render(request, 'users/index.html', context=context)


class IndexWarnView(View):
    """
    首页异步加载最新4条预警信息
    """

    def get(self, request):
        id = request.GET.get('id', '')
        if id:
            try:
                new_warn = NewWarn.objects.get(id=id)
            except Exception as e:
                return restful.result(message='找不到id')
            else:
                serializers = IndexWarnSerializers(new_warn)
                data = serializers.data
                return restful.result(data=data)
        else:
            try:
                # 删除过期的首页预警数据 -- 30分钟过期
                now_time = datetime.datetime.now() + datetime.timedelta(minutes=-30)
                outtime_data = NewWarn.objects.filter(add_time__lte=now_time)
                if outtime_data.exists():
                    for i in outtime_data:
                        i.delete()
                new_warns = NewWarn.objects.all()[:4]
                serializers = NewWarnSerializers(new_warns, many=True)
                data = serializers.data
                return restful.result(data=data)
            except Exception as e:
                return restful.params_error(message=e)


class LogView(UserAuthMixin, View):
    permission_required = 'public.view_userlog'
    """
    渲染操作日志页面
    """

    def get(self, request):
        return render(request, 'public/log.html')


class UserLogView(View):
    """
    日志操作
    """

    def get(self, request):
        """
        返回操作日志数据
        :param request:
        :return:
        """
        try:
            user_log = UserLog.objects.all()
            log_count = user_log.count()
            user_log = rec_page(request, user_log)
            serializers = UserLogSerializers(user_log, many=True)
            data = serializers.data
            return restful.result(code=0, count=log_count, data=data)
        except Exception as e:
            return restful.params_error(message=e)

    def post(self, request):
        """
        删除日志
        :param request:
        :return:
        """
        try:
            data_value = request.POST.get('data_list', '')
            if data_value:
                id_int = eval(data_value)
                if type(id_int) == int:
                    warn = UserLog.objects.using('users').get(id=id_int)
                    warn.delete()
                    return restful.result()
                else:
                    data_list = list(id_int)
                    for i in data_list:
                        warn = UserLog.objects.using('users').get(id=i)
                        warn.delete()
                    return restful.result()
        except Exception as e:
            return restful.params_error(message=e)


def index_warn(resource_id, event_id, image_path, list_data):
    """
    保存首页预警实例
    :param resource_id:
    :param event_id:
    :param image_path:
    :return:
    """
    path = 'https://obs-swj.obs.cn-east-2.myhuaweicloud.com/'
    try:
        name = Map.objects.get(resource_id=resource_id).name
    except:
        name = '设备{0}号'.format(resource_id[-2:])
    else:
        image_url = path + image_path
        new_warn = NewWarn(
            name=name,
            image_url=image_url,
            event_id=event_id,
            image_sign=str(list_data))
        new_warn.save()


class RecDataView(RecImage, View):
    """
    smn云端下发预警消息，post请求接受处理,获取数据保存本地数据表
    """

    def post(self, request):
        hw_http = HwHttp(type=1, add_time=time.time())
        hw_http.save()

        # 这里判断是手动还是智能预警，若是用户手动标记预警，warn_type值由前端js提供. 1.智能预警  2.手动预警
        warn_type = request.POST.get('warn_type', 1)
        if warn_type == 1:
            rec_data = request.body
            rec_data = str(rec_data, encoding='utf-8')
            rec_data = json.loads(rec_data)
            type_id = rec_data['type_id']
            resource_id = rec_data['resource_id']
            image_path = rec_data['result_info']['result_list'][0]['obs_path']
            event_id1 = time.strftime("%Y%m%d%H%M%S", time.localtime())+mixin.random_str(2)
            x = rec_data['result_info']['result_list'][0]['object_list'][0]['x']
            y = rec_data['result_info']['result_list'][0]['object_list'][0]['y']
            w = rec_data['result_info']['result_list'][0]['object_list'][0]['w']
            h = rec_data['result_info']['result_list'][0]['object_list'][0]['h']
            list_data = [x, y, w, h]
            index_warn(resource_id, event_id1, image_path, list_data)
            event_id2 = time.strftime("%Y%m%d%H%M%S", time.localtime())+mixin.random_str(2)
            is_day = rec_data['is_day']
            start_time = rec_data['result_info']['result_list'][0][
                'object_list'][0]['startTime']
            end_time = rec_data['result_info']['result_list'][0][
                'object_list'][0]['endTime']
            start_time = int(start_time / 1000)
            end_time = int(end_time / 1000)
            try:
                dev_id = Map.objects.get(resource_id=resource_id).dev_id
            except Exception as e:
                return restful.params_error(message=e)
        else:
            dev_id = request.POST.get('dev_id', '')
            end_time = int(time.time())
            start_time = end_time - 8
            resource_id = 'water_' + dev_id
            event_id1 = time.strftime("%Y%m%d%H%M%S", time.localtime())+mixin.random_str(2)
            event_id2 = time.strftime("%Y%m%d%H%M%S", time.localtime())+mixin.random_str(2)
            type_id = '0'
            image_path = '手动预警'
            list_data = '手动预警'
            is_day = 2

        rec_data = {
            'event_id1': event_id1,
            'event_id2': event_id2,
            'dev_id': dev_id,
            'end_time': end_time,
            'start_time': start_time,
            'resource_id': resource_id,
            'type_id': type_id,
            'warn_type': warn_type,
            'image_path': image_path,
            'list_data': list_data,
            'is_day': is_day
        }
        copy_data = {
            'event_id1': event_id1,
            'event_id2': event_id2,
        }

        cache.set(event_id1, rec_data, 30 * 60)  # 请求截图和视频数据存到缓存中 - 有效期30分钟
        cache.set(event_id2, copy_data, 30 * 60)  # 请求截图和视频数据存到缓存中 - 有效期30分钟
        try:
            rec_image = RecImage()
            rec_image.send_data(
                dev_id=dev_id,
                s_date=start_time,
                s_date_end=end_time,
                event_id1=event_id1,
                event_id2=event_id2)

            hw_http = HwHttp(type=2, add_time=time.time())
            hw_http.save()

            return restful.result()
        except Exception as e:
            return restful.params_error(message=e)


class RecMediaView(View):
    """
    接受返回的截图和视频数据
    """

    def post(self, request):

        hw_http1 = ZwHttp1(type=1, add_time=time.time())
        hw_http1.save()

        rec_data = request.body
        rec_data = str(rec_data, encoding='utf-8')
        rec_data = json.loads(rec_data)
        event_id = rec_data['body']['event_id']
        data = cache.get(event_id)  # 从缓存中读取数据
        event_id1 = data['event_id1']  # 传给截图的id
        event_id2 = data['event_id2']  # 传给视频的id
        if event_id == event_id1:
            try:
                rec_image = rec_data['body']['pic_urls']
            except Exception:
                return restful.params_error(message='图片列表为空')
            else:
                data = cache.get(event_id1)
                if data.get('video_url', ''):
                    data.update({'rec_image': rec_image})
                    self.save_data(data, event_id1, event_id2)
                else:
                    cache.delete(event_id1)
                    data.update({'rec_image': rec_image})
                    cache.set(event_id1, data, 30 * 60)
                    hw_http2 = ZwHttp1(type=2, add_time=time.time())
                    hw_http2.save()
                    return restful.result()

        elif event_id == event_id2:
            try:
                video_url = rec_data['body']['vedio_url']
            except Exception:
                return restful.params_error(message='视频列表为空')
            else:
                data = cache.get(event_id1)
                if data.get('rec_image', ''):
                    data.update({'video_url': video_url})
                    self.save_data(data, event_id1, event_id2)
                else:
                    cache.delete(event_id1)
                    data.update({'video_url': video_url})
                    cache.set(event_id1, data, 30 * 60)
                    hw_http2 = ZwHttp1(type=2, add_time=time.time())
                    hw_http2.save()
                    return restful.result()
        return restful.result()

    def save_data(self, data, event_id1, event_id2):
        resource_id = data['resource_id']
        type_id = data['type_id']
        start_time = data['start_time']
        end_time = data['end_time']
        warn_type = data['warn_type']
        video_url = data['video_url']
        rec_image = data['rec_image']
        rec_image = rec_image.split(';')[:-1]
        warn_url = data['image_path']
        image_sign = data['list_data']
        is_day = data['is_day']
        start_time1 = datetime.datetime.fromtimestamp(start_time)

        # 处理获取的图片列表，保存在本地数据表WarnImage中，并通过外检找到对应的预警模型WarnModel
        try:
            map = Map.objects.get(resource_id=resource_id)
            type = WarnType.objects.get(type_id=str(type_id))
            warn = WarnModel(
                start_time=int(start_time),
                end_time=int(end_time),
                video_url=video_url,
                event_id=event_id1,
                is_day=int(is_day),
                warn_type=warn_type,
                warn_url=warn_url,
                image_sign=image_sign,
                add_time=start_time1)
        except Exception as e:
            return restful.params_error(message=e)
        else:
            warn.map = map
            warn.warn_manage = type
            warn.save()
            try:
                # 遍历所有得到的抓拍图片 - 保存.
                for image_url in rec_image:
                    warn_image = WarnImage()
                    warn_image.image_url = image_url
                    warn_image.warn_image = warn
                    warn_image.save()
            except Exception:
                return restful.params_error(message='保存预警图片失败...')
            else:
                cache.delete(event_id1)  # 取完数据删除
                cache.delete(event_id2)

                hw_http3 = ZwHttp1(type=2, add_time=time.time())
                hw_http3.save()
                try:
                    NewWarn.objects.get(
                        event_id=event_id1).delete()  # 删除首页已存的预警数据
                except:
                    pass
                return restful.result()


class CityTreeView(View):
    """
    组合数据以地区树展示
    """

    def get(self, request):
        city = CityDict.objects.all()
        serializers = CityDictSerializers(city, many=True)
        data = serializers.data
        citys = JSONRenderer().render(data)
        citys = json.loads(citys, encoding='utf-8')
        is_true = {'spread': 'true'}
        citys[0].update(is_true)
        citys[1].update(is_true)
        citys[2].update(is_true)
        citys[3].update(is_true)
        for i in range(len(citys)):
            citys[i]['children'] = []

        city_dict = {}

        for d in citys:
            id = d.get('id')
            city_dict[id] = d

        for k in city_dict:
            parent_category = city_dict[k][
                'parent_category']  # 找到parent_category
            if parent_category:
                city_dict[parent_category]['children'].append(city_dict[k])

        res_list = []
        for i in city_dict:
            if not city_dict[i]['parent_category']:
                res_list.append(city_dict[i])

        # 城市树以后再优化。。。
        for i in res_list:
            if i['children']:
                for j in i['children']:
                    if j['children']:
                        for x in j['children']:
                            x['children'] = x.pop('maps')
        return restful.result(data=res_list)


class BdMapView(View):
    """
    百度地图返回json数据
    """

    def get(self, request):
        bdmap = Map.objects.all()
        serializer = BdMapSerializers(bdmap, many=True)
        data = serializer.data
        return restful.result(data=data)


class SelectDevView(View):
    """
    返回预警分析页 监控点筛选数据
    """

    def get(self, request):
        try:
            all_map = Map.objects.values('id', 'name')
            serializers = MapSelectSerializers(all_map, many=True)
            data = serializers.data
            return restful.result(data=data)
        except Exception as e:
            return restful.params_error(message=e)


class SendDataView(View):
    # 上报预警至城管系统

    def post(self, request):
        try:

            # 前端获取预警id,然后拼接参数，请求城管平台
            dev_id = request.POST.get('dev_id', '')
            id = request.POST.get('id', '')
            event_id = request.POST.get('event_id', '')
            images = request.POST.get('images', '')  # 是个list
            images = eval(images)
            video_url = request.POST.get('video_url', '')
            map_name = request.POST.get('map_name', '')

            warn_url = request.POST.get('warn_url', '')  # 预警标注图片
            map = Map.objects.get(dev_id=dev_id)
            username = request.user.username  # 任务分派人
            upload_date = time.strftime(" %Y-%m-%d %H:%M:%S")
            # 减去偏差值
            gisx = map.longitude - 0.010764738  # 经度
            gisy = map.latitude - 0.003760059  # 维度
            url = []
            attachname = mixin.random_str()
            for image in images:
                pic_data = {
                    "attachurl": image['image_url'],
                    "attachtype": "picture",
                    "attachname": attachname + '.jpg'
                }
                url.append(pic_data)

            if warn_url == '手动预警':
                warn_data = {
                    "attachurl": "手动预警没有事件图片",
                    "attachtype": "picture",
                    "attachname": attachname + '.jpg'
                }
                url.append(warn_data)
            else:
                warn_data = {
                    "attachurl": "https://obs-swj.obs.cn-east-2.myhuaweicloud.com/" + warn_url,
                    "attachtype": "picture",
                    "attachname": attachname + '.jpg'
                }
                url.append(warn_data)

            paras = {
                "sourcenum": event_id,
                "url": url,
                "username": username,
                "upload_date": upload_date,
                "gisx": gisx,
                "gisy": gisy,
                "description": "视频地址：" + video_url,
                "seriousdegree": "1",
                "infotype": "事件",
                "bigclass": "01",
                "smallclass": "0126",
                "smallclassname": "河道污染",
                "positiondesc": map_name,
            }
            jsons = {
                "SenderCode": "5",
                "ValidateData": "Epoint**##0456",
                "paras": paras
            }
            try:
                request_url = "http://2.40.7.3:8086/gs-citywebservice/rest/CaseService/uploadcase"
                headers = {
                    "Content-Type": "application/json",
                }
                response = requests.post(url=request_url, json=jsons, headers=headers)
                result = response.content
                result = str(result, encoding='utf-8')
                result = json.loads(result)
                # 请求城管平台成功，响应内容result
                # print(result)

                code = int(result['ReturnInfo']['Code'])
                if code == 1:
                    warn_obj = WarnModel.objects.get(id=int(id))
                    warn_obj.is_make = 2
                    warn_obj.result = '处理中'
                    warn_obj.user = request.user.username
                    warn_obj.save()
                    return restful.result()
                else:
                    # 当响应的code为0，则表示上传到城管平台失败
                    # 上报失败，返回400，弹窗上报失败
                    return restful.params_error(message='上报失败...')
            except Exception as e:
                return restful.params_error(message='网络请求失败，上报失败...')
        except Exception as e:
            return restful.params_error(message='上报城管平台失败...')


class RecManageView(View):
    """
    城管平台上报工单更新状态
    请求body
    event_id
    status : {
    1：办理中
    0：已作废
    2：已办理
    }
    progress
    staff
    feedback
    """

    def post(self, request):
        rec_data = request.body
        try:
            rec_data = str(rec_data, encoding='utf-8')
            rec_data = json.loads(rec_data)
            # 根据城管提交来的数据，匹配对象，修改对象字段内容
            event_id = rec_data['event_id']
            # 需要判断这个event_id 在不在已发送的记录中
            try:
                warn_object = WarnModel.objects.get(event_id=event_id)
            except Exception as e:
                data = {
                    "status": 1,
                    "postscript": 'Please check your event_id'
                }
                return restful.result(data=data)
            if warn_object.is_make == 2:
                manage_user = rec_data['staff']
                status = rec_data['status']
                result = rec_data['progress']
                status = int(status)
                try:
                    # 正常状态下，可以给城管平台成功的响应
                    # data :{
                    # status
                    # postscript
                    # }
                    warn_obj = WarnModel.objects.get(event_id=event_id)
                    warn_obj.manage_user = manage_user
                    if status == 0:
                        # 丢弃预警状态
                        warn_obj.is_make = 4
                        warn_obj.result = result
                        warn_obj.save()
                        data = {
                            "status": 0,
                            "postscript": 0
                        }
                        return restful.result(data=data)
                    elif status == 1:
                        # 已完成状态，反馈图片，需要显示
                        warn_obj.is_make = 3
                        warn_obj.result = result
                        try:
                            feedback = rec_data['feedback']
                        except Exception as e:
                            data = {
                                "status": 1,
                                "postscript": 'Please upload feedback pictures'

                            }
                            return restful.result(data=data)
                        count = len(feedback)
                        if count == 0:
                            data = {
                                "status": 1,
                                "postscript": 'Please upload feedback pictures'

                            }
                            return restful.result(data=data)

                        warn_obj.save()
                        for image in feedback:
                            manage_images = ManageImage()
                            manage_images.images_url = image
                            manage_images.manage_image = warn_obj
                            manage_images.save()
                        data = {
                            "status": 0,
                            "postscript": 0
                        }

                        return restful.result(data=data)
                    else:
                        data = {
                            "status": 1,
                            "postscript": 'Please check your parameters'

                        }

                        return restful.result(data=data)

                except Exception as e:
                    # 将异常记录到日志里
                    # 城管平台请求抓拍系统失败，返回
                    data = {
                        "status": 1,
                        "postscript": '请求抓拍系统失败'
                    }
                    return restful.result(data=data)
            else:
                data = {
                    "status": 1,
                    "postscript": '请确定当前预警是否在需要反馈列表中'
                }
                return restful.result(data=data)
        except Exception as e:
            data = {
                "status": 1,
                "postscript": 'Please check your parameters'
            }
            return restful.result(data=data)
