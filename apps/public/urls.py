from django.urls import path

from apps.public import views, data_views

app_name = 'public'

urlpatterns = [
    path('log/', views.LogView.as_view(), name='log'),
    path('user_log/', views.UserLogView.as_view(), name='user_log'),
    path('city_tree/', views.CityTreeView.as_view(), name='city_tree'),
    path('bdmap/', views.BdMapView.as_view(), name='bdmap'),
    path('index_warn/', views.IndexWarnView.as_view(), name='index_warn'),
    path('select_dev/', views.SelectDevView.as_view(), name='select_dev'),
    path('send_data/', views.SendDataView.as_view(), name='send_data'),
    path('rec_data', views.RecDataView.as_view(), name='rec_data'),
    path('rec_media', views.RecMediaView.as_view(), name='rec_media'),
    path('rec_manage', views.RecManageView.as_view(), name='rec_manage'),
    path('top_five/', data_views.TopFiveView.as_view(), name='top_five'),
    path('top_three/', data_views.TopThreeView.as_view(), name='top_three'),
    path('warn_type/', data_views.WarnTypeView.as_view(), name='warn_type'),
    path('line_data/', data_views.LineDataView.as_view(), name='line_data'),
    path('column_data/', data_views.ColumnDataView.as_view(), name='column_data'),
    path('cake_data/', data_views.CakeDataView.as_view(), name='cake_data'),
    path('http_data/', data_views.HttpDataView.as_view(), name='http_data'),
    path('index_data/', data_views.IndexDataView.as_view(), name='index_data')
]
