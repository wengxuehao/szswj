from django.core import signing  # 生成token加密和解密算法
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from utils.user_log import get_user_log
from utils.mixin import UserAuthMixin
from utils import restful

from .forms import LoginForm, RoleForm, UserAdminForm, UserModifyForm
from .models import User, UserGroup
from .user_prems import add_manage, auth_perm
from .serializers import UserSerializer, UserGroupSerializer, GroupSerializer


@method_decorator(csrf_protect, name='dispatch')
class LoginView(View):
    """
    登录逻辑
    """

    def get(self, request):
        """
        访问登录页面
        """
        print(11111111111)
        return render(request, 'users/login.html')

    def post(self, request):
        """
        登录请求处理
        """
        print(222222222222)
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username,
                                password=password)
            if user:
                login(request, user)
                to_url = auth_perm(user)
                detail = "用户: ({0}) 执行了 <登录> 操作.".format(request.user.username)
                get_user_log(request, 4, detail)
                return redirect(reverse(to_url))
            else:
                return render(request, 'users/login.html', {'message': '账号密码错误,请重试.'})
        else:
            return render(request, 'users/login.html', {'message': '验证失败,请重试.'})
            # return redirect(reverse('users:login'))


class LogoutView(View):
    """
    退出逻辑
    """

    def get(self, request):
        """
        退出请求处理
        """
        detail = "用户: ({0}) 执行了 <退出> 操作.".format(request.user.username)
        get_user_log(request, 5, detail)
        logout(request)
        return redirect(reverse('users:login'))


# 用户管理页面
class UserManageView(UserAuthMixin, View):
    permission_required = 'users.view_user'

    def get(self, request):
        return render(request, 'users/user_manage.html')


class UserAdminView(View):
    """
    用户管理员相关视图
    """

    def get(self, request):
        """
        get查询所有用户,返回json数据
        """
        user = User.objects.all()
        serializers = UserSerializer(user, many=True)
        data = serializers.data
        return restful.result(data=data, code=0)

    def post(self, request):
        """
        创建用户
        """
        try:
            user_form = UserAdminForm(request.POST)
            if user_form.is_valid():
                group_id = request.POST.get('group_id', '')
                if not group_id:
                    return restful.params_error(message='请选择分组...')
                username = user_form.cleaned_data['username']
                email = user_form.cleaned_data['email']
                password = make_password(user_form.cleaned_data['password'])
                user = User.objects.create(username=username, email=email, password=password)
                detail = "用户: ({0}) 执行了 用户名：{1} 的 <增加> 操作.".format(request.user.username, username)
                get_user_log(request, 1, detail)
                try:
                    group = Group.objects.get(id=group_id)
                    user.groups.add(group)
                    return restful.result()
                except Exception:
                    return restful.params_error(message='设置权限失败，请重试...')
            else:
                return restful.params_error(message=user_form.get_errors())
        except Exception as e:
            return restful.server_error(message=e)

    def delete(self, request):
        """
        删除用户
        :return:
        """
        id = str(request.body, encoding='utf-8').split('=')[1]
        try:
            user = User.objects.get(id=int(id))
            detail = "用户: ({0}) 执行了 用户名：{1} 的 <删除> 操作.".format(request.user.username, user.username)
            get_user_log(request, 3, detail)
            user.delete()
            return restful.result()
        except Exception as e:
            return restful.server_error(message=e)


class UserDataView(View):
    """
    单个用户信息操作
    """

    def post(self, request):
        """
        更新用户分组信息
        :param request:
        :return:
        """
        try:
            id = request.POST.get('id', '')
            group_id = request.POST.get('group_id', '')
        except:
            return restful.params_error(message='值为空,请重新输入.')
        else:
            user = User.objects.get(id=int(id))
            group = Group.objects.get(id=int(group_id))
            user.groups.clear()
            user.groups.add(group)
            user.save()
            detail = "用户: ({0}) 执行了 用户名：{1} 的 <修改> 操作.".format(request.user.username, user.username)
            get_user_log(request, 2, detail)
            return restful.result()


class ModifyPasswordView(View):
    """
    修改密码
    """

    def post(self, request):
        try:
            user_id = request.POST.get('user_id', '')
        except:
            return restful.params_error(message='获取用户id失败,请重试.')
        pwd_form = UserModifyForm(request.POST)
        if pwd_form.is_valid():
            password = pwd_form.cleaned_data['password']
            user = User.objects.get(id=int(user_id))
            user.password = make_password(password)
            user.save()
            return restful.result()
        else:
            return restful.params_error(message=pwd_form.get_errors())


class UserGroupView(View):
    """
    用户角色相关视图
    """

    def get(self, request):
        """
        get查询所有用户角色,返回json数据
        """
        groups = UserGroup.objects.all()
        serializers = UserGroupSerializer(groups, many=True)
        data = serializers.data
        return restful.result(data=data, code=0)

    def post(self, request):
        """
        增加角色和权限
        """
        role_form = RoleForm(request.POST)
        try:
            if role_form.is_valid():
                name = role_form.cleaned_data.get('name')
                desc = role_form.cleaned_data.get('desc')
                user_groups = UserGroup()
                groups = Group.objects.create(name=name)
                detail = "用户: ({0}) 执行了 角色名：{1} 的 <增加> 操作.".format(request.user.username, name)
                get_user_log(request, 3, detail)
                user_groups.desc = desc
                user_groups.group = groups
                check_val = request.POST.get('check_val')
                check_val = eval(check_val)
                if isinstance(check_val, int):
                    perm_one = add_manage(check_val)
                    for i, data in enumerate(perm_one):
                        try:
                            groups.permissions.add(data)
                        except Exception as e:
                            for j, data_son in enumerate(data):
                                groups.permissions.add(data_son)
                    user_groups.save()
                    return restful.result()
                elif isinstance(check_val, tuple):
                    check_val = list(check_val)
                    perm_list = add_manage(check_val)
                    for i, data in enumerate(perm_list):
                        try:
                            groups.permissions.add(data)
                        except Exception as e:
                            for j, data_son in enumerate(data):
                                groups.permissions.add(data_son)
                    user_groups.save()
                    return restful.result()
                detail = "用户: ({0}) 执行了 角色名：{1} 的 <增加> 操作.".format(request.user.username, name)
                get_user_log(request, 1, detail)
                return restful.result()
            else:
                return restful.params_error(message=role_form.get_errors())
        except Exception as e:
            return restful.params_error(message=e)

    def delete(self, request):
        """
        删除角色
        """
        id = str(request.body, encoding='utf-8').split('=')[1]
        try:
            user_group = UserGroup.objects.get(id=int(id))
            detail = "用户: ({0}) 执行了 角色名：{1} 的 <删除> 操作.".format(request.user.username, user_group.group.name)
            get_user_log(request, 3, detail)
            user_group.group.delete()
            user_group.delete()
            return restful.result()
        except Exception as e:
            return restful.server_error(message=e)


class RoleUpdateView(View):
    """
    修改角色信息
    """

    def post(self, request):
        try:
            id = request.POST.get('id', '')
            name = request.POST.get('name', '')
        except Exception as e:
            return restful.params_error(message='参数错误')
        else:
            group = Group.objects.get(id=id)
            group.name = name
            group.save()
            return restful.result()


class RecUserGroupView(View):
    """
    点击查看角色权限文字叙述
    """

    def get(self, request):
        try:
            group_id = request.GET.get('group_id', '')
            groups = UserGroup.objects.get(id=group_id)
            perm_data = groups.group.permissions.all()
            perm_list = {}
            for index, data in enumerate(perm_data):
                perm_dict = {
                    '权限{0}'.format(index + 1): data.name
                }
                perm_list.update(perm_dict)
            return restful.result(data=perm_list)
        except Exception as e:
            return restful.params_error(message=e)


class UserGroupNameView(View):
    """
    返回角色组数据
    """

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        data = serializer.data
        return restful.result(data=data)


class UserTokenView(View):
    """
    返回token
    """

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            token = signing.dumps({username: password})
            cache.set(username, token, 5 * 60)  # token有效期为5分钟
            data = {
                'username': username,
                'Token': token
            }
            return restful.result(data=data)
        else:
            return restful.result()


class AuthTokenView(View):
    """
    验证token,执行其他逻辑
    """

    def post(self, request):
        token = request.POST.get('token', '')
        try:
            token = cache.get(token)
        except Exception as e:
            return restful.params_error(message='token验证失败，请重新获取token')
        if token:
            pass
        return restful.result()
