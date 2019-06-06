from django.views.generic.base import View

from .models import Map
from .forms import MapNameForm
from utils import restful


# 地图坐标-信息
class MapNameView(View):
    """
    修改监控点名称
    """
    def post(self, request):
        try:
            map_form = MapNameForm(request.POST)
            if map_form.is_valid():
                id = request.POST.get('id')
                name = map_form.cleaned_data['name']
                map = Map.objects.get(id=id)
                map.name = name
                map.save()
                return restful.result()
            else:
                return restful.params_error(message=map_form.get_errors())
        except Exception:
            return restful.params_error(message=map_form.get_errors())
