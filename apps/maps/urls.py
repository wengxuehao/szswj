from django.urls import path

from .views import MapNameView


app_name = 'maps'

urlpatterns = [
    path('map_name/',MapNameView.as_view(),name='map_name'),
]