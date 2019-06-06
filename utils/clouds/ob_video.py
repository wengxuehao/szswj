import time
import json
from random import Random

import requests
from django.conf import settings

from apps.maps.models import Map
from apps.public.models import ZwHttp2, HwHttp, ZwHttp1


class CloudMixin:
    """
    初始化一些全局设置
    """

    def __init__(self, *args, **kwargs):
        """
        初始化以后调用云平台接口，获取token,user_id
        :param dev_id:
        """
        self.form_headers = settings.FORM_RESULT
        self.json_headers = settings.JSON_RESULT
        self.account = settings.ACCOUNT
        self.password = settings.PASSWORD
        self.conn_sum = settings.CONN_NUMBER
        self.rec_url = settings.REC_URL
        self.conn_url = settings.CONN_URL
        self.vis_url = settings.VIS_URL
        self.video_url = settings.VIDEO_URL
        self.image_url = settings.IMAGE_URL
        self.play_url = settings.PLAY_URL
        self.stop_play_url = settings.STOP_PLAY_URL
        self.search_video_url = settings.SEARCH_VIDEO_URL
        self.play_video_url = settings.PLAY_VIDEO_URL
        self.stop_video_url = settings.STOP_VIDEO_URL
        self.time_out = settings.TIME_OUT
        self.status = True

        self.user_data = {'account': self.account, 'passwd': self.password}

    def random_str(self, random_length=6):
        """
        生成6位随机数
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


class UserAuth(CloudMixin):
    """
    获取云平台用户token/user_id
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        pass

    def get_user(self):
        while True:
            try:
                body_data = requests.post(
                    url=self.rec_url,
                    data=self.user_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端设备列表
                body_data = body_data.content
                body_data = str(body_data, encoding='utf-8')
                body_data = json.loads(body_data)
                access_token = body_data['body']['access_token']
                user_id = body_data['body']['user_id']
                self.access_token = access_token
                self.user_id = user_id

                self.json_headers.update({
                    'X-Auth-Token': 'access_token'
                })  # 获取token ，并保存

                if body_data['ret'] != 0:
                    raise ValueError('云平台用户验证失败，请稍后重试~')

                break  # 验证成功，终止while循环，执行后面的逻辑代码

            except requests.exceptions.ConnectionError:

                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))

                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return self.status
                continue
        return True


class CloudVideo(UserAuth):
    """
    获取时光云平台设备信息,并同步到本地主模型接口,加入异常捕捉，
    若远程接口网络出问题，可重新访问3次，最后返回页面，提示用户重试。
    注：数据以云平台为主，若本地数据与云数据有误，同步所有云数据。
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        pass

    def get_ob_video(self, dev_id=None):
        """
        同步远程监控信息
        :return:
        """

        if self.get_user():
            """
            判断获取token, user_id值是否正确
            """

            token_data = {
                'access_token': self.access_token,
                'user_id': self.user_id
            }

            self.token_data = token_data
        else:
            self.token_data = {}

        self.conn_sum = settings.CONN_NUMBER  # 初始化重连数
        while True:
            try:
                json_data = requests.get(
                    url=self.conn_url,
                    params=self.token_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端设备列表
                json_data = json_data.content
                json_data = str(json_data, encoding='utf-8')
                json_data = json.loads(json_data)

                if json_data['ret'] != 0:
                    raise ValueError('验证失败')
                else:
                    break  # 验证成功，终止while循环，执行后面的逻辑代码

            except requests.exceptions.ConnectionError as e:
                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return self.status
                continue

        json_data = (json_data['body']['dev_list'])

        dev_id = []  # 云端设备id列表
        status_cloud = []  # 云端设备状态列表

        # 获取云端所有设备Id,放入列表中
        for i in range(len(json_data)):
            dev_id.append(json_data[i]['id'])
            status_cloud.append(json_data[i]['status'])

        map = Map.objects.values('dev_id')
        map_id = []  # 读取本地监控点主模型设备id
        cloud_id = []  # 获取云端设备id列表

        for i, data in enumerate(map):
            map_id.append(data['dev_id'])
        """
        获取云端数据并同步到本地数据表
        """
        for i in range(len(json_data)):
            cloud_id.append(json_data[i]['id'])
            if str(json_data[i]['id']) in map_id:
                # 在此同步云端数据　- status / longitude / latitude / address
                try:
                    map = Map.objects.get(dev_id=json_data[i]['id'])
                    map.status = json_data[i]['status']
                    map.longitude = float(json_data[i]['longitude'])
                    map.latitude = float(json_data[i]['latitude'])
                    map.address = json_data[i]['address']
                    map.save()
                except Exception as e:
                    print('获取失败！')
                    print(e)

            else:
                map = Map()
                # map.name = json_data[i]['name']  # 监控点名称
                print(json_data[i]['id'])
                map.name = '设备{0}号'.format(i)  # 监控点名称
                map.longitude = json_data[i]['longitude']  # 经度
                map.latitude = json_data[i]['latitude']  # 纬度
                map.dev_id = json_data[i]['id']  # 设备id
                map.status = int(json_data[i]['status'])  # 设备状态
                map.address = '监控点{0}号'.format(i)  # 地址
                map.resource_id = str('water_{0}'.format(
                    json_data[i]['id']))  # 后期上线需要成获取云端设备
                map_id.append(json_data[i]['id'])
                map.save()
                map.save()

        # 判断云端若删除设备,本地也做删除操作
        if len(map_id) > len(cloud_id):
            # del_id = [dev_id for dev_id in map_id if not dev_id in cloud_id]
            del_id = set(map_id) - set(cloud_id)
            Map.objects.filter(dev_id__in=list(del_id)).delete()

        # 上面代码已经完全同步本地和云端设备信息。

        return self.status


class RecVis(UserAuth):
    """
    获取云端设备流vis地址
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        pass

    def rec_vis(self, dev_id=None):
        """
        获取云端设备流vis地址
        :param dev_id:
        :return:
        """

        if self.get_user():
            """
            判断获取token, user_id值是否正确
            """

            token_data = {
                'access_token': self.access_token,
                'user_id': self.user_id
            }

            dev_data = {'dev_id': str(dev_id)}
            token_data.update(dev_data)
            self.token_data = token_data

        else:
            self.token_data = {}

        self.conn_sum = settings.CONN_NUMBER  # 初始化重连数

        while True:
            try:
                rec_data = requests.post(
                    url=self.vis_url,
                    data=self.token_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端设备vis

                rec_data = rec_data.content
                rec_data = str(rec_data, encoding='utf-8')
                rec_data = json.loads(rec_data)
                stream_name = rec_data['stream_name']

                if rec_data.status_code != 0:
                    raise ValueError('验证失败~')
                break  # 验证成功，终止while循环，执行后面的逻辑代码
            except requests.exceptions.ConnectionError:
                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return self.status
                continue
        return stream_name


class RecImage(UserAuth):
    """
    获取云平台截取图片和视频
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        pass

    def send_data(self,
                  dev_id=None,
                  s_date=None,
                  s_date_end=None,
                  count=5,
                  event_id1=None,
                  event_id2=None,
                  action_image='snapshot',
                  action_video='cut'):
        """
        发送云平台截取视频/图片数据
        """
        if self.get_user():
            """
            判断获取token, user_id值是否正确
            """

            token_data = {
                'access_token': self.access_token,
                'user_id': self.user_id
            }
            dev_data = {
                'dev_id': str(dev_id),
                's_date': int(s_date),
                's_date_end': int(s_date_end),
            }
            token_data.update(dev_data)

        else:
            token_data = {}
            self.token_image_data = {}
            self.token_video_data = {}

        self.conn_sum = settings.CONN_NUMBER  # 初始化重连数

        while True:
            try:
                # ******************** 发送截取图片数据开始 ********************

                image = {'count': int(count), 'action': action_image, 'event_id': event_id1}
                token_data.update(image)
                self.token_image_data = token_data

                hw_http = ZwHttp2(type=1, category=1, add_time=time.time())
                hw_http.save()

                image_data = requests.get(
                    url=self.image_url,
                    params=self.token_image_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端抓拍图片列表　多个
                image_data = image_data.json()
                rec_image = image_data['ret']
                if rec_image != 0:
                    raise ValueError('发送截图请求失败，请重试...')

                # ******************** 发送截取图片数据结束 *****************

                # ******************** 获取截取视频开始 ********************

                hw_http = ZwHttp2(type=2, category=1, add_time=time.time())
                hw_http.save()

                token_data.pop('action')
                token_data.pop('count')
                token_data.pop('event_id')

                video = {'action': action_video, 'event_id': event_id2}

                token_data.update(video)

                self.token_video_data = token_data

                hw_http = ZwHttp2(type=1, category=2, add_time=time.time())
                hw_http.save()

                video_data = requests.get(
                    url=self.video_url,
                    params=self.token_video_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端抓拍视频 1个
                video_data = video_data.json()
                rec_video = video_data['ret']
                if rec_image != 0:
                    raise ValueError('发送视频截取失败，请重试...')

                # ******************** 获取截取视频结束 ********************

                hw_http = ZwHttp2(type=2, category=2, add_time=time.time())
                hw_http.save()

                break  # 验证成功，终止while循环，执行后面的逻辑代码
            except requests.exceptions.ConnectionError:
                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return (self.status,)
                continue
        return rec_image, rec_video


class RecVideo(UserAuth):
    """
    获取云平台设备播放地址
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        pass

    def rec_play(self, dev_id=None, video_type=None, byNetwork=None):
        """
        获取播放地址
        :param dev_id:
        :param video_type:
        :return:
        """
        if self.get_user():
            """
            判断获取token, user_id值是否正确
            """

            token_data = {
                'access_token': self.access_token,
                'user_id': self.user_id
            }

            dev_data = {'dev_id': str(dev_id), 'video_type': '0'}
            token_data.update(dev_data)
            self.token_data = token_data

        else:
            self.token_data = {}

        self.conn_sum = settings.CONN_NUMBER  # 初始化重连数

        while True:
            try:
                rec_data = requests.post(
                    url=self.play_url,
                    data=self.token_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端设备播放地址
                rtmp_data = rec_data.content
                rtmp_data = str(rtmp_data, encoding='utf-8')
                rtmp_data = json.loads(rtmp_data)
                rtmp_str = rtmp_data['body']['mrts']['v_ip']
                rtmp_url = json.loads(rtmp_str)
                rtmp_url = rtmp_url['urls']['rtmp']
                monitor_id = rtmp_data['body']['monitor_id']
                self.rtmp_url = rtmp_url
                self.monitor_id = monitor_id

                if rtmp_data['ret'] != 0:
                    raise ValueError('验证失败~')
                break  # 验证成功，终止while循环，执行后面的逻辑代码
            except requests.exceptions.ConnectionError:
                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return (self.status,)
                continue
        return self.rtmp_url, self.monitor_id

    def stop_play(self, monitor_id=None):
        """
        发送暂停播放请求
        :param monitor_id:
        :return:
        """

        if self.get_user():
            """
            判断获取token, user_id值是否正确
            """

            token_data = {
                'access_token': self.access_token,
                'user_id': self.user_id
            }

            dev_data = {'monitor_id': str(monitor_id)}
            token_data.update(dev_data)
            self.token_data = token_data

        else:
            self.token_data = {}

        self.conn_sum = settings.CONN_NUMBER  # 初始化重连数

        while True:
            try:
                rec_data = requests.post(
                    url=self.stop_play_url,
                    data=self.token_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 发送停止播放指令
                rtmp_data = rec_data.content
                rtmp_data = str(rtmp_data, encoding='utf-8')
                rtmp_data = json.loads(rtmp_data)

                if rtmp_data['ret'] != 0:
                    raise ValueError('验证失败~')
                break  # 验证成功，终止while循环，执行后面的逻辑代码
            except requests.exceptions.ConnectionError:
                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return self.status
                continue
        return True


class SearchVideo(UserAuth):
    """
    对录像相关操作接口
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        pass

    def search_video(self, dev_id=None, s_date=None, s_date_end=None, rec_type=0):
        """
        查询某一天的可播放录像时间
        :param dev_id:
        :param s_date:
        :param rec_type:
        :return:
        """
        if self.get_user():
            """
            判断获取token, user_id值是否正确
            """

            token_data = {
                'access_token': self.access_token,
                'user_id': self.user_id
            }

            dev_data = {
                'dev_id': dev_id,
                's_date': s_date,
                's_date_end': s_date_end,
                'rec_type': rec_type,
            }
            token_data.update(dev_data)
            self.token_data = token_data
        else:
            self.token_data = {}

        self.conn_sum = settings.CONN_NUMBER  # 初始化重连数

        while True:
            try:
                rec_data = requests.get(
                    url=self.search_video_url,
                    params=self.token_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端设备列表
                rec_data = rec_data.json()
                start_time = rec_data['body']['his_recs']
                end_time = rec_data['body']['his_recs']

                if rec_data['ret'] != 0:
                    raise ValueError('验证失败~')
                break  # 验证成功，终止while循环，执行后面的逻辑代码
            except requests.exceptions.ConnectionError:
                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return (self.status,)
                continue
        return start_time, end_time

    def play_video(self, dev_id=None, start_time=None, stop_time=None, rec_type=0):
        """
        请求播放视频录像
        :param dev_id:
        :param start_time:
        :param end_time:
        :param rec_type:
        :return:
        """
        if self.get_user():
            """
            判断获取token, user_id值是否正确
            """

            token_data = {
                'access_token': self.access_token,
                'user_id': self.user_id
            }

            dev_data = {
                'dev_id': dev_id,
                'start_time': start_time,
                'stop_time': stop_time,
                'rec_type': rec_type,
                'chan_id': '1'
            }
            token_data.update(dev_data)
            self.token_data = token_data
        else:
            self.token_data = {}

        self.conn_sum = settings.CONN_NUMBER  # 初始化重连数

        while True:
            try:
                rec_data = requests.post(
                    url=self.play_video_url,
                    data=self.token_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端播放录像
                video_data = rec_data.content
                video_data = str(video_data, encoding='utf-8')
                video_data = json.loads(video_data)
                monitor_id = video_data['body']['monitor_id']
                rtmp_data = video_data['body']['mrts']['v_ip']
                rtmp_data = json.loads(rtmp_data)
                rtmp_url = rtmp_data['urls']['rtmp']

                if video_data['ret'] != 0:
                    raise ValueError('验证失败~')
                break  # 验证成功，终止while循环，执行后面的逻辑代码
            except requests.exceptions.ConnectionError:
                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return (self.status,)
                continue
        return monitor_id, rtmp_url

    def stop_video(self, monitor_id=None):
        """
        停止播放视频录像
        :param monitor_id:
        :return:
        """
        if self.get_user():
            """
            判断获取token, user_id值是否正确
            """

            token_data = {
                'access_token': self.access_token,
                'user_id': self.user_id
            }

            dev_data = {
                'monitor_id': str(monitor_id),
            }
            token_data.update(dev_data)
            self.token_data = token_data
        else:
            self.token_data = {}

        self.conn_sum = settings.CONN_NUMBER  # 初始化重连数

        while True:
            try:
                rec_data = requests.post(
                    url=self.stop_video_url,
                    data=self.token_data,
                    headers=self.form_headers,
                    timeout=self.time_out)  # 获取云端设备列表
                video_data = rec_data.content
                video_data = str(video_data, encoding='utf-8')
                video_data = json.loads(video_data)

                if video_data['ret'] != 0:
                    raise ValueError('验证失败~')
                break  # 验证成功，终止while循环，执行后面的逻辑代码
            except requests.exceptions.ConnectionError:
                print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
                time.sleep(1)
                self.conn_sum -= 1
                if self.conn_sum == 0:
                    self.status = False
                    return self.status
                continue
        return True


def send_vis(dev_id=None):
    """
    接受设备号，处理返回vis地址
    :param dev_id:
    :return:
    """
    stream_name = str('water_{0}'.format(dev_id))
    return stream_name
