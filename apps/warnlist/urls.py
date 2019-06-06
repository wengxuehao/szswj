from django.urls import path

from . import views

app_name = 'warnlist'

urlpatterns = [
    path('', views.WarnListView.as_view(), name='warn_list'),
    path('rec_data/', views.WarnDataView.as_view(), name='rec_data'),
    path('sum/', views.SumListViews.as_view(), name='sum_list'),
    path('manage/', views.WarnManageView.as_view(), name='manage'),
    path('stream/', views.NewStreamView.as_view(), name='stream'),
    path('manages/',views.WarnProcessView.as_view(),name='warn_manage'),
    path('search_manage/', views.SearchManageView.as_view(), name='search_manage'),
    path('new_manage/', views.NewManageView.as_view(), name='new_manage'),
    path('del_manage/', views.NewManageView.as_view(), name='del_manage'),
    path("newsum_list/",views.SumSelectViews.as_view(),name='newsum_list'),
    path("warn_image/",views.WarnImageView.as_view(),name='warn_image'),
    path("manage_image/",views.ManageImageView.as_view(),name='manage_image'),
]