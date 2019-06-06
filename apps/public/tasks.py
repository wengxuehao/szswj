# # __author__ : htzs
# # __time__   : 19-4-19 上午9:40
#
# import json, time
# from django.core.cache import cache
# from utils import restful, mixin
# from apps.maps.models import Map
# from utils.clouds.ob_video import RecImage
# from celery import shared_task
#
#
# @shared_task
# def cloud_data(rec_data, warn_type, request):
#     """
#     异步接受告警上报，储存在memcached中
#     :param rec_data:
#     :param warn_type:
#     :param request:
#     :return:
#     """
#     if warn_type == 1:
#         rec_data = str(rec_data, encoding='utf-8')
#         rec_data = json.loads(rec_data)
#         resource_id = rec_data['resource_id']
#         type_id = rec_data['type_id']
#         start_time = rec_data['result_info']['result_list'][0]['object_list'][0]['startTime']
#         end_time = rec_data['result_info']['result_list'][0]['object_list'][0]['endTime']
#         start_time = int(start_time / 1000)
#         end_time = int(end_time / 1000)
#         event_id = mixin.random_str()
#         try:
#             dev_id = Map.objects.get(resource_id=resource_id).dev_id
#         except Exception as e:
#             return restful.params_error(message=e)
#
#     else:
#         dev_id = request.POST.get('dev_id', '')
#         end_time = int(time.time())
#         start_time = end_time - 10
#         resource_id = 'water_' + dev_id
#         event_id = mixin.random_str()
#         type_id = '1'
#
#     rec_data = {
#         'event_id': event_id,
#         'dev_id': dev_id,
#         'end_time': end_time,
#         'start_time': start_time,
#         'resource_id': resource_id,
#         'type_id': type_id
#     }
#
#     cache.set(event_id, rec_data, 15 * 60)  # 拿到数据存到缓存中 - 有效期30分钟
#
#     try:
#         rec_image = RecImage()
#         # rec_image.send_data(dev_id=dev_id, s_date=start_time, s_date_end=end_time, event_id1=event_id)
#         rec_image.send_data(dev_id=dev_id, s_date=1555912960, s_date_end=1555912969, event_id1=event_id)
#     except Exception as e:
#         return restful.params_error(message=e)
#
