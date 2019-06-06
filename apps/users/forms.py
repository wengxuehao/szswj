from django import forms

from utils.error_forms import FormMixin
from .models import User


class LoginForm(forms.Form, FormMixin):
    """
    登陆用户
    """
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)


class RoleForm(forms.Form, FormMixin):
    """
    创建角色
    """
    name = forms.CharField(max_length=30)
    desc = forms.CharField(max_length=300)


class UserAdminForm(forms.ModelForm, FormMixin):
    """
    创建用户
    """
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class UserModifyForm(forms.Form, FormMixin):
    """
    修改用户
    """
    password = forms.CharField(min_length=6, max_length=30)

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) <= 6:
            raise forms.ValidationError('密码最少为6位')
        return data