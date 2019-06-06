from rest_framework import serializers

from apps.maps.models import Map, CityDict
from apps.warnlist.models import WarnModel
from apps.video.serializers import PlaySerializers, VideoSerializers


class MapSerializers(serializers.ModelSerializer):
    warn_count = serializers.SerializerMethodField()

    """
    地图序列化
    """

    class Meta:
        model = Map
        fields = ('id', 'dev_id', 'resource_id', 'name', 'warn_count', 'address', 'city', 'video')

    def get_warn_count(self, obj):
        return obj.warnmodel_set.filter(is_make=1).count()


class BdMapSerializers(serializers.ModelSerializer):
    """
    百度地图序列化
    """
    video = serializers.CharField(source='play.video')
    monitor_id = serializers.CharField(source='play.monitor_id')
    warn_count = serializers.SerializerMethodField()

    class Meta:
        model = Map
        fields = ('id', 'name', 'dev_id', 'address', 'video', 'monitor_id',
                  'warn_count', 'longitude', 'latitude', 'status', 'address',
                  'add_time')

    def get_warn_count(self, obj):
        return obj.warnmodel_set.filter(is_make=1).count()


class MapSelectSerializers(serializers.ModelSerializer):
    """
    地图序列化
    """

    class Meta:
        model = Map
        fields = ('id', 'name')


class CityDictSerializers(serializers.ModelSerializer):
    """
    地区序列化
    """
    maps = MapSerializers(many=True, read_only=True)

    # warn_sum = BdMapSerializers(source='warn_count')

    class Meta:
        model = CityDict
        fields = ('id', 'name', 'maps', 'category_type', 'parent_category')
