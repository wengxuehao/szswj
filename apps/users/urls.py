from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('manage/', views.UserManageView.as_view(), name='user_manage'),
    path('user_group/', views.UserGroupView.as_view(), name='user_group'),
    path('user_admin/', views.UserAdminView.as_view(), name='user_admin'),
    path('user_data/', views.UserDataView.as_view(), name='user_data'),
    path('rec_group/', views.RecUserGroupView.as_view(), name='rec_group'),
    path('all_group/', views.UserGroupNameView.as_view(), name='all_group'),
    path('auth_token/', views.UserTokenView.as_view(), name='auth_token'),
    path('role_update/', views.RoleUpdateView.as_view(), name='role_update'),
    path('modify_password/', views.ModifyPasswordView.as_view(), name='modify_password'),
]
