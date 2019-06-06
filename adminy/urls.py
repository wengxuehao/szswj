"""adminy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from apps.public.views import IndexView
from django.views.static import serve
from adminy.settings import MEDIA_ROOT, DEBUG


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(),name='index'),
    path('users/', include('apps.users.urls')),
    path('maps/', include('apps.maps.urls')),
    path('public/',include('apps.public.urls')),
    path('video/', include('apps.video.urls')),
    path('warn_list/', include('apps.warnlist.urls')),
]

if DEBUG:
    urlpatterns += [
        re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    ]
else:
    from adminy.settings import STATIC_ROOT
    urlpatterns += [
        re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
        re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    ]