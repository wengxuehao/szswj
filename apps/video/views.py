import time, json

from django.shortcuts import render
from django.views.generic.base import View

from .models import Play
from apps.maps.models import Map
from utils import restful
from utils.clouds.ob_video import CloudVideo, RecVideo, SearchVideo
from utils.user_log import get_user_log
from utils.mixin import UserAuthMixin


class VideoView(UserAuthMixin, View):
    """
    视频监控页
    """
    permission_required = 'video.view_video'

    def get(self, request):
        """
        获取监控点坐标信息
        """
        map_sum = Map.objects.all().count()
        map_good = Map.objects.filter(status=1).count()
        map_fail = Map.objects.filter(status=0).count()
        show_maps = Map.objects.filter(status=0).values('name')

        context = {
            'map_sum': map_sum,
            'map_good': map_good,
            'map_fail': map_fail,
            'show_maps': show_maps
        }
        return render(request, 'video/video.html', context=context)


class VideoHomeView(UserAuthMixin, View):
    """
    视频墙页
    """
    permission_required = 'video.change_video'

    def get(self, request):
        return render(request, 'video/video_home.html')


class WatchVideoView(View):
    def get(self, request):
        return render(request, 'video/view_video.html')


class VideoManageView(UserAuthMixin, CloudVideo, View):
    """
    监控管理页
    """
    permission_required = 'video.change_play'

    def get(self, request):
        """
        获取所有设备并同步云端数据
        :param request:
        :return:
        """
        if self.get_ob_video():
            map_sum = Map.objects.all().count()
            map_good = Map.objects.filter(status=1).count()
            map_fail = Map.objects.filter(status=0).count()
            show_maps = Map.objects.filter(status=0).values('name')

            context = {
                'map_sum': map_sum,
                'map_good': map_good,
                'map_fail': map_fail,
                'show_maps': show_maps
            }
            return render(request, 'video/video_manage.html', context=context)
        else:
            return render(request, 'video/video_manage.html')


class RecPlayView(RecVideo, View):
    """
    获取直播播放地址 - rtmp格式
    """
    def post(self,request):
        try:
            dev_id = request.POST.get('dev_id', '')
            map = Map.objects.get(dev_id=dev_id)
        except:
            return restful.result()
        try:
            rtmp_url, monitor_id = self.rec_play(dev_id=dev_id)
        except:
            return restful.result()
        else:
            try:
                Play.objects.all().delete()
                play = Play()
                play.video = rtmp_url
                play.monitor_id = monitor_id
                play.map = map
                play.save()
                detail = "用户: ({0}) 执行了<设备id:{1}> <直播查看> 操作.".format(request.user.username, dev_id)
                get_user_log(request, 6, detail)
                rtmp_url = rtmp_url.replace(rtmp_url[7:18], '119.3.19.254')
                return restful.result(data={'rtmp_url': rtmp_url})
            except:
                return restful.result()


class StopPlayView(RecVideo, View):
    """
    停止播放直播流
    """
    def post(self, request):
        try:
            monitor_id = request.POST.get('monitor_id','')
            self.stop_play(monitor_id=monitor_id)
        except:
            return restful.result(message='停止失败,请重试.')
        else:
            Play.objects.filter(monitor_id=monitor_id).delete()
            return restful.result()


class SearchVideoView(SearchVideo, View):
    """
    查询录像
    """
    def get(self, request):
        """
        前端获取日期，默认只查询一天之间的录像
        :param request:
        :return:
        """
        date_value = request.GET.get('date_value', '')
        time_tuple = time.strptime(date_value, "%Y-%m-%d")
        start_time = int(time.mktime(time_tuple))
        end_time = int(start_time + 86400)
        dev_id = request.GET.get('dev_id', '')
        if dev_id:
            try:
                # 得到时间区间元组
                data = self.search_video(dev_id=dev_id, s_date=start_time, s_date_end=end_time)
                json_value = []
                for index, value in enumerate(data[0]):
                    json_value.append({'title': '{0}.'.format(index + 1)})
                    json_value[index].update(value)
                json_data = json.dumps(json_value, ensure_ascii=False)
                return restful.result(data=json_data)
            except Exception as e:
                return restful.params_error(message=e)
        else:
            return restful.params_error(message='请先选择监控点.')


class PlayVideoView(SearchVideo, View):
    """
    播放录像
    """
    def post(self, request):
        try:
            dev_id = request.POST.get('dev_id','')
            start_time = request.POST.get('start_time','')
            stop_time = request.POST.get('stop_time','')
            data = self.play_video(dev_id=dev_id, start_time=start_time, stop_time=stop_time)
            if data:
                monitor_id = data[0]
                rtmp_url = data[1]
                rtmp_url = rtmp_url.replace(rtmp_url[7:18], '119.3.19.254')
                data = {
                    'monitor_id': monitor_id,
                    'rtmp_url': rtmp_url
                }
            else:
                return restful.result(message='获取失败,请重试.')
        except Exception as e:
            return restful.params_error(message=e)
        detail = "用户: ({0}) 执行了<设备id:{1}> <录像查看> 操作.".format(request.user.username, dev_id)
        get_user_log(request, 6, detail)
        return restful.result(data=data)


class StopVideoView(SearchVideo, View):
    """
    停止播放录像
    """
    def post(self, request):
        try:
            monitor_id = request.POST.get('monitor_id', '')
            data = self.stop_video(monitor_id=monitor_id)
        except Exception as e:
            return restful.params_error(message=e)
        return restful.result(data=data)
