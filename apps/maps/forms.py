# __author__ : htzs
# __time__   : 19-4-17 下午3:01

from django import forms

from utils.error_forms import FormMixin


class MapNameForm(forms.Form, FormMixin):
    name = forms.CharField(max_length=8)

