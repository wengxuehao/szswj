import logging, json

from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q

from utils import restful
from utils.watergo.ob_huawei import AnalysisMixin, RecWarnType
from apps.maps.models import Map
from .models import WarnModel, WarnType, WarnManage, StreamId
from .serializers import WarnSerializers, WarnTypeSerializers, WarnProcessSerializers, ManageWarnSerializers, \
    ManageImageSerializers, WarnImageSerializers
from utils.page_func import rec_page
from utils.user_log import get_user_log
from utils.mixin import UserAuthMixin

logger = logging.getLogger('diango')


class WarnListView(UserAuthMixin, View):
    """
    预警分析页
    """

    permission_required = 'warnlist.view_warnmodel'

    def get(self, request):
        """
        加载页面
        """
        return render(request, 'warnlist/warnlist.html')


class WarnDataView(View):
    """
    预警分析页异步渲染数据
    """

    def get(self, request):
        """
        js请求渲染数据
        :param request:
        :return:
        """
        check_value = request.GET.get('check_value', '')
        check_dev = request.GET.get('check_dev', '')
        check_manage = request.GET.get('check_manage', '')
        check_day = request.GET.get('check_day', '')
        warn_list = WarnModel.objects.filter(is_make=1)
        # 判断任务筛选值
        if len(check_manage) == 1:
            warn_list = warn_list.filter(warn_manage=int(check_manage))
        if len(check_manage) == 2:
            warn_list = warn_list.filter(warn_manage=int(check_manage))
        # 判断预警筛选值
        if len(check_value) == 1:
            warn_list = warn_list.filter(warn_type=int(check_value))
        # 判断时间筛选值
        if len(check_day) == 1:
            warn_list = warn_list.filter(is_day=int(check_day))
        # 判断监控点筛选值
        if len(check_dev) == 1:
            warn_list = warn_list.filter(map_id=int(check_dev))
        elif len(check_dev) > 0:
            try:
                check_dev = list(eval(check_dev))
                warn_list = warn_list.filter(map_id__in=check_dev)
            except Exception:
                check_dev = eval(check_dev)
                warn_list = warn_list.filter(map_id=check_dev)
        warn_sum = warn_list.count()
        warn_data = rec_page(request, warn_list)
        serializers = WarnSerializers(warn_data, many=True)
        data = serializers.data
        return restful.result(data=data, count=warn_sum, code=0)

    def post(self, request):
        """
        将预警信息改为已丢弃
        :param reuqest:
        :return:
        """
        try:
            id = request.POST.get('id', '')
            data_value = request.POST.get('data_list', '')
            if id and not data_value:
                warn = WarnModel.objects.get(id=id)
                warn.is_make = 5
                warn.result = '已丢弃'
                warn.user = request.user.username
                warn.save()
                detail = "用户: ({0}) 执行了<预警编号:{1}> <修改> 操作.".format(request.user.username, warn.event_id)
                get_user_log(request, 2, detail)
                return restful.result()
            elif data_value and not id:
                id_int = eval(data_value)
                if type(id_int) == int:
                    warn = WarnModel.objects.get(id=id_int)
                    warn.is_make = 5
                    warn.result = '已丢弃'
                    warn.user = request.user.username
                    warn.save()
                    detail = "用户: ({0}) 执行了<预警编号:{1}> <修改> 操作.".format(request.user.username, warn.event_id)
                    get_user_log(request, 2, detail)
                    return restful.result()
                else:
                    data_list = list(id_int)
                    for i in data_list:
                        warn = WarnModel.objects.get(id=i)
                        warn.is_make = 5
                        warn.result = '已丢弃'
                        warn.user = request.user.username
                        warn.save()
                        detail = "用户: ({0}) 执行了<预警编号:{1}> <修改> 操作.".format(request.user.username, warn.event_id)
                        get_user_log(request, 2, detail)
                    return restful.result()
        except Exception as e:
            return restful.params_error(message=e)


class SumListViews(UserAuthMixin, View):
    """
    数据统计页
    """
    permission_required = 'warnlist.view_warntype'

    def get(self, request):
        return render(request, 'warnlist/sum_list.html')


class SumSelectViews(View):
    def get(self, request):
        is_make = request.GET.get("is_make")
        is_make = int(is_make)
        try:
            if is_make == 3:
                warn_list = WarnModel.objects.filter(is_make=is_make)
                warn_data = rec_page(request, warn_list)
                serializers = ManageWarnSerializers(warn_data, many=True)
            elif is_make == 4:
                warn_list = WarnModel.objects.filter(Q(is_make=4) | Q(is_make=5))
                warn_data = rec_page(request, warn_list)
                serializers = WarnSerializers(warn_data, many=True)
            else:
                warn_list = WarnModel.objects.filter(is_make=is_make)
                warn_data = rec_page(request, warn_list)
                serializers = WarnSerializers(warn_data, many=True)
            warn_sum = warn_list.count()
            data = serializers.data
            return restful.result(data=data, count=warn_sum, code=0)
        except Exception as e:
            return restful.params_error(message=e)


class WarnProcessView(UserAuthMixin, View):
    """
    任务管理页
    """
    permission_required = 'warnlist.view_warnmanage'

    def get(self, request):
        """
        加载页面
        """
        return render(request, 'warnlist/warn-manage.html')


class WarnManageView(AnalysisMixin, View):
    """
    任务管理页面返回Json数据给前端渲染
    """

    def get(self, request):
        """
        获取所有任务 使用本地数据表来渲染页面信息
        :param request:
        :return:
        """
        try:
            process_list = WarnManage.objects.all()
            process_count = process_list.count()
            process_data = rec_page(request, process_list)
            serializers = WarnProcessSerializers(process_data, many=True)
            data = serializers.data
            return restful.result(data=data, count=process_count, code=0)
        except Exception as e:
            return restful.params_error(message=e)


class NewStreamView(AnalysisMixin, View):
    """
    创建视频流
    """

    def post(self, request):
        resource_id = None
        self.search_stream()
        try:
            resource_id = request.POST.get('resource_id', 0)
            stream_id = self.create_stream(resource_id=resource_id)
            if stream_id:
                StreamId(stream_id=stream_id, resource_id=resource_id).save()
                json_data = {'stream_id': stream_id}
                data = json.dumps(json_data, ensure_ascii=False)
                return restful.result(data=data)
            else:
                try:
                    stream = StreamId.objects.get(resource_id=resource_id)
                    stream_id = stream.stream_id
                    json_data = {'stream_id': stream_id}
                    data = json.dumps(json_data, ensure_ascii=False)
                    return restful.result(data=data)
                except Exception as e:
                    return restful.params_error(message=e)
        except Exception as e:
            return restful.params_error(message=e)


class NewManageView(AnalysisMixin, View):
    """
    创建分析任务
    """

    def post(self, request):
        """
        获取前端提供的值type_id, stream_id, resource_id
        :param request:
        :return:
        """
        resource_id = request.POST.get('resource_id', '')
        type_list = request.POST.get('type_id', '')  # 这是个列表
        type_id = type_list.split(',')
        for i in type_id:
            stream_id = request.POST.get('stream_id', '')
            process_id = self.create_process(stream_id=stream_id, type_id=i)
            if process_id:
                try:
                    warn_manage = WarnManage()
                    type = WarnType.objects.get(type_id=i)
                    map = Map.objects.get(resource_id=resource_id)
                    stream_id = StreamId.objects.get(stream_id=stream_id)
                    warn_manage.stream = stream_id
                    warn_manage.type = type
                    warn_manage.map = map
                    warn_manage.process_id = process_id
                    warn_manage.type_name = type.get_type_name_display()
                    warn_manage.save()
                    detail = "用户: ({0}) 执行了<分析任务:{1}> <增加> 操作.".format(request.user.username, warn_manage.type_name)
                    get_user_log(request, 1, detail)
                except Exception as e:
                    return restful.params_error(message=e)
            else:
                # continue
                return restful.result(message='已经创建，可以跳过了')
        return restful.result(message='创建成功')

    def delete(self, request):
        """
        删除任务
        :param request:
        :return:
        """
        process_id = request.body
        process_id = str(process_id, encoding='utf-8')
        process_id = process_id.split('=')[1]
        result = self.del_process(process_id=process_id)

        if result:
            try:
                warn_manage = WarnManage.objects.get(process_id=process_id)
                warn_manage.delete()
                detail = "用户: ({0}) 执行了<分析任务:{1}> <删除> 操作.".format(request.user.username, warn_manage.type_name)
                get_user_log(request, 6, detail)
                return restful.result()
            except Exception as e:
                return restful.params_error(message=e)
        else:
            try:
                warn_manage = WarnManage.objects.get(process_id=process_id)
                warn_manage.delete()
                return restful.result(message='本地删除成功')
            except:
                return restful.result(message='删除出错')


class SearchManageView(RecWarnType, View):
    """
    返回所有分析类型json数据
    """

    def get(self, request):
        try:
            # self.make_sync()  # 先查询并更新云端最新预警任务类型列表
            warn_type = WarnType.objects.all()
            serializers = WarnTypeSerializers(warn_type, many=True)
            data = serializers.data
            return restful.result(data=data)
        except Exception as e:
            return restful.params_error(message=e)


class WarnImageView(View):
    """
    返回预警图片
    """

    def get(self, request):
        try:
            id = request.GET.get('id', '')
            warn_image = WarnModel.objects.get(id=id)
            images = warn_image.images.values('image_url')
            if images.exists():
                serializer = WarnImageSerializers(images, many=True)
                data = serializer.data
                return restful.result(data=data)
            else:
                return restful.result(message='本预警暂无图片，请重试...')
        except:
            return restful.result(message='参数错误，请重试...')


class ManageImageView(View):
    """
    返回城管预警图片
    """

    def get(self, request):
        try:
            id = request.GET.get('id', '')
            warn_image = WarnModel.objects.get(id=id)
            images = warn_image.manage_images.values('images_url')
            if images.exists():
                serializer = ManageImageSerializers(images, many=True)
                data = serializer.data
                return restful.result(data=data)
            else:
                return restful.result(message='本预警暂无图片，请重试...')
        except:
            return restful.result(message='参数错误，请重试...')
