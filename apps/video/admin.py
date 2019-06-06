from django.contrib import admin

from .models import Play, Video


class PlayAdmin(admin.ModelAdmin):
    list_display = ['id', 'map', 'video', 'monitor_id', 'add_time']


class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'map', 'video', 'monitor_id', 'add_time']


admin.site.register(Play, PlayAdmin)

admin.site.register(Video, VideoAdmin)
