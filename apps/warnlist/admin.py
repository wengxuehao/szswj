from django.contrib import admin

from .models import WarnModel, WarnImage, WarnType, WarnManage, StreamId, NewWarn, ManageImage


class WarnAdmin(admin.ModelAdmin):
    list_display = ['is_day', 'event_id', 'map', 'warn_manage', 'warn_type', 'start_time',
                    'end_time', 'user', 'manage_user', 'video_url', 'warn_url', 'image_sign', 'is_make', 'result', 'add_time']
    search_fields = ['event_id', 'map']
    list_filter = ['event_id', 'map', 'warn_manage']


admin.site.register(WarnModel, WarnAdmin)


class WarnImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_url', 'warn_image', 'add_time']


admin.site.register(WarnImage, WarnImageAdmin)


class ManageImageAdmin(admin.ModelAdmin):
    list_display = ['images_url', 'manage_image', 'add_time']


admin.site.register(ManageImage, ManageImageAdmin)


class NewWarnAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_id', 'image_url', 'image_sign', 'add_time']


admin.site.register(NewWarn, NewWarnAdmin)


class WarnTypeAdmin(admin.ModelAdmin):
    list_display = ['type_id', 'type_name', 'desc', 'add_time']


admin.site.register(WarnType, WarnTypeAdmin)


class WarnManageAdmin(admin.ModelAdmin):
    list_display = ['type', 'map', 'process_id', 'type_name', 'desc', 'add_time']


admin.site.register(WarnManage, WarnManageAdmin)


class StreamIdAdmin(admin.ModelAdmin):
    list_display = ['stream_id', 'resource_id', 'add_time']


admin.site.register(StreamId, StreamIdAdmin)
