from django.contrib import admin

from .models import UserLog, HwHttp, ZwHttp1, ZwHttp2


class UserLogAdmin(admin.ModelAdmin):
    using = 'users'

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    list_display = ['user', 'user_type', 'ip_address', 'desc', 'add_time']


admin.site.register(UserLog, UserLogAdmin)


class HwHttpAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'add_time']


admin.site.register(HwHttp, HwHttpAdmin)


class ZwHttp1Admin(admin.ModelAdmin):
    list_display = ['id', 'type', 'add_time']


admin.site.register(ZwHttp1, ZwHttp1Admin)


class ZwHttp2Admin(admin.ModelAdmin):
    list_display = ['id', 'type', 'category', 'add_time']


admin.site.register(ZwHttp2, ZwHttp2Admin)
