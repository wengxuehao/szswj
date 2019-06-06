# __author__ : htzs
# __time__   : 19-4-2 上午9:43


from rest_framework import serializers

from .models import UserLog


class UserLogSerializers(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(format="%Y/%m/%d %H:%M", required=False, read_only=True)
    user_type = serializers.CharField(source='get_user_type_display')

    class Meta:
        model = UserLog
        fields = ('id', 'user', 'ip_address', 'user_type', 'desc', 'add_time')
