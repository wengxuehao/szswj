# __author__ : htzs
# __time__   : 19-3-5 下午4:31
import requests
import time

from adminy import settings
from adminy.settings import Result_address
from apps.warnlist.models import WarnType
from utils import restful
from utils.set_data import read_data


class AnalysisMixin:
    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        url = 'https://iam.cn-east-2.myhuaweicloud.com/v3/auth/tokens'
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": "szsswj",
                            "password": "abc123",
                            "domain": {
                                "name": "szsswj"
                            }
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": "cn-east-2"
                    }
                }
            }
        }
        response = requests.post(url=url, json=data, headers=headers)
        token = response.headers['X-Subject-Token']
        self.headers = {
            'X-Auth-Token': token,
            'Content-Type': 'application/json;charset=utf-8'
        }
        self.conn_sum = settings.WATER_CONN_NUMBER
        self.type_url = settings.WATER_TYPE_URL
        self.process_url = settings.WATER_PROCESS_URL
        self.stream_url = settings.WATER_STREAM_URL
        self.match_result_url = settings.WATER_MATCH_RESULT_URL
        self.time_out = settings.TIME_OUT
        self.alarm_url = settings.NEW_ALARM_URL
        self.alarm_id = settings.ALARM_ID

    def get_types(self):
        """
        查询所有的检测类型
        :return:
        """
        try:
            response = requests.get(url=self.type_url, headers=self.headers)
            result = response.json()
            types_list = result['types']
            return types_list
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            types_list = None
            return types_list

        except Exception as e:
            return restful.server_error(message='请求失败，请重试...')

    def get_models(self):
        """
        查询所有检查模型
        :return:
        """
        try:
            response = requests.get(url=self.type_url, headers=self.headers)
            result = response.json()
            total_count = len(result['models'])
            models_list = result['models']
            return total_count, models_list
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            return restful.server_error(message='请求失败，请重试...')

    def create_stream(self, resource_id=None):
        """
        创建视频流
        resource_id--拿到管理平台的VIS的stream_name
        响应拿到视频流id，用作下发任务
        :param resource_id:
        :return:
        """
        data = {
            "resource_id": resource_id,
            "resource_type": "VIS",
            'longitude': 111,
            'latitude': 16,
            'description': '111',
        }
        try:
            response = requests.post(url=self.stream_url, json=data, headers=self.headers)
            result = response.json()
            result_code = response.status_code
            if result_code == 400:
                return False
            else:
                stream_id = result['stream_id']
                return stream_id
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            return restful.server_error(message='请求失败，请重试...')

    def del_stream(self, stream_id):
        """
        删除视频流
        :param stream_id:
        :return:
        """
        params = {
            "stream_id": stream_id
        }
        try:
            response = requests.delete(url=self.stream_url + '/{0}'.format(stream_id), headers=self.headers)
            # 返回响应状态码204
            return response.status_code
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            return restful.server_error(message='请求失败，请重试...')

    def search_stream(self):
        """
        查询视频流列表
        :return:
        """
        data = {
            "offset": 1,
            'limit': 10,
        }
        try:
            response = requests.get(url=self.stream_url, data=data, headers=self.headers)
            result = response.json()
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            return restful.server_error(message='请求失败，请重试...')

    def create_process(self, type_id=None, stream_id=None):
        """
        创建模型匹配任务
        :param type_id:
        :param stream_id:
        :return:
        """
        json_data = read_data(stream_id=stream_id)
        data = {
            "result_address": Result_address,
            "stream_id": stream_id,
            "type_id": type_id,
            'revise_time': 10,
            'alarm_id': self.alarm_id,
            'detect_night': 0,
            "config": json_data
        }

        try:
            response = requests.post(url=self.process_url, json=data, headers=self.headers)
            result_code = response.status_code
            if result_code == 400:
                return False
            else:
                result = response.json()
                process_id = result['id']
                return process_id
        except:
            return restful.server_error(message='请求失败.')

    def del_process(self, process_id=None):
        """
        删除任务
        :param process_id:
        :return:
        """
        params = {
            "process_id": process_id
        }
        try:
            result = requests.delete(url=self.process_url + '/{0}'.format(process_id), headers=self.headers)
            result_code = result.status_code
            if result_code == 204:
                return True
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            return False

    def get_process(self):
        """
        响应数据
        total_count
        processes的列表
        :return:
        """
        try:
            response = requests.get(url=self.process_url, headers=self.headers)
            result = response.json()
            total_count = result['total_count']
            process_list = result['processes']
            return process_list
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            time.sleep(1)
            self.conn_sum -= 1
            if self.conn_sum == 0:
                self.status = False
                return self.status
            return restful.server_error(message='请求失败，请重试...')

    def match_result(self):
        """
        查询模型匹配结果
        :return:
        """

        response = requests.get(url=self.match_result_url, headers=self.headers)
        result = response.json()
        total_count = len(result['match_results'])
        match_results = result['match_results']
        return total_count, match_results

    def new_alarm(self):
        """
        创建上报方式
        """
        data = {
            "protocol": 'http',
            "endpoint": "http://119.3.42.90:8080/public/rec_data/",
            'description': '苏州抓拍系统预警接收端口'
        }

        try:
            response = requests.post(url=self.alarm_url, json=data, headers=self.headers)
            result = response.json()
            result_code = response.status_code
            if result_code == 400:
                return False
            else:
                return True
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            return restful.server_error(message='请求失败，请重试...')

    def del_alarm(self):
        """
        删除上报方式
        :param :
        :return:
        """
        try:
            result = requests.delete(url=self.alarm_url + '/{0}'.format(self.alarm_id), headers=self.headers)
            result_code = result.status_code
            if result_code == 204:
                return True
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            return False

    def search_alarm(self):
        """
        查询上报方式
        """
        data = {
            "protocol": 'http',
            "endpoint": "http://119.3.42.90:8080/public/rec_data/"
        }

        try:
            response = requests.get(url=self.alarm_url, json=data, headers=self.headers)
            result = response.json()
            result_code = response.status_code
            if result_code == 400:
                return False
            else:
                return True
        except requests.exceptions.ConnectionError:
            print('接口链接异常，第 {0} 次尝试重连中...'.format(self.conn_sum))
            return restful.server_error(message='请求失败，请重试...')


# 暂时不用了 华为要更新其他商户 本项目固定2个
class RecWarnType(AnalysisMixin):
    """
    获取华为云分析任务类型列表，并同步本地
    """

    def __init__(self):
        super().__init__()
        pass

    def make_sync(self):
        try:
            rec_data = self.get_types()
            local_warn_type = []
            local_data = WarnType.objects.values('type_id')
            # 获取本地任务模型数量
            for i in range(local_data.count()):
                local_warn_type.append(local_data[i]['type_id'])

            # 获取云端任务模型数量，并同步到本地
            for i in range(len(rec_data)):
                if rec_data[i]['id'] in local_warn_type:
                    continue
                elif int(rec_data[i]['id']) == 10:
                    continue
                else:
                    warn_type = WarnType()
                    warn_type.type_id = rec_data[i]['id']
                    warn_type.type_name = rec_data[i]['description']
                    warn_type.desc = rec_data[i]['name']
                    warn_type.save()
        except Exception as e:
            print('Error:{0}'.format(e))
        return True
