from django.contrib import admin

from .models import Map, CityDict


class MapAdmin(admin.ModelAdmin):
    list_display = ['id','name','dev_id', 'resource_id','status','longitude','latitude','address','city']


class CityAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'category_type','parent_category','add_time']


admin.site.register(Map,MapAdmin)

admin.site.register(CityDict,CityAdmin)

