from django.urls import path

from . import views

app_name = 'video'

urlpatterns = [
    path('', views.VideoView.as_view(), name='video'),
    path('video_home/', views.VideoHomeView.as_view(), name='video_home'),
    path('view_video/', views.WatchVideoView.as_view(), name='view_video'),
    path('video_manage/', views.VideoManageView.as_view(), name='video_manage'),
    path('rec_play/', views.RecPlayView.as_view(), name='rec_play'),
    path('stop_play/', views.StopPlayView.as_view(), name='stop_play'),
    path('search_video/', views.SearchVideoView.as_view(), name='search_video'),
    path('play_video/', views.PlayVideoView.as_view(), name='play_video'),
    path('stop_video/', views.StopVideoView.as_view(), name='stop_video'),
]
