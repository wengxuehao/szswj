"""
Django settings for adminy project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os, sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5o95f13g40v5*xvg5od!lwq@s@^eqn6v)!dofg9cgoa)k+=egd'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

# ALLOWED_HOSTS = ['127.0.0.1', '119.3.42.90', '172.16.0.9']
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.users',
    'apps.video',
    'apps.maps',
    'apps.warnlist',
    'apps.public',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middle_phone.MobileMiddleware',  # 静止手机访问网页
    'utils.middle_auth.AuthMiddleWare'  # 访问限制
]

ROOT_URLCONF = 'adminy.urls'

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/users/login/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'adminy.wsgi.application'

# 数据库读写分离配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'adminy',
        'USER': 'root',
        'PASSWORD': 'admin123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        }
    },

    'users': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'adminy',
        'USER': 'root',
        'PASSWORD': 'admin123',
        'HOST': '172.16.0.9',
        'PORT': '3306',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        }
    }
}

DATABASE_ROUTERS = ['utils.auth_router.AuthRouter']  # 用户数据路由

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_FUNCTION': lambda key, prefix_key, version: "django:%s" % key,
        'MAX_ENTRIES': 500
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Age of cookie, in seconds (default: 2 weeks).
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if DEBUG:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

"""
访问时光云接口配置项 开始
"""

CONN_NUMBER = 3  # 视频设备id接口重连次数

REC_URL = 'http://119.3.15.54/vcloud/open/user/login/'  # 获取用户token

CONN_URL = 'http://119.3.15.54/vcloud/open/device/mylist/'  # 获取设备列表接口Url

DEV_URL = 'http://119.3.15.54/vcloud/open/device/deviceinfo/'  # 获取单个设备接口Url

CHANGE_URL = 'http://119.3.15.54/vcloud/open/device/changename/'  # 修改设备名称

STATUS_URL = 'http://119.3.15.54/vcloud/open/device/getstatus/'  # 获取设备状态

CAPTURE_URL = 'http://119.3.15.54/vcloud/open/device/getstatus/'  # 设备照相图片抓取

VIS_URL = 'http://119.3.15.54/vcloud/open/media/getvis/'  # 获取设备流vis

IMAGE_URL = 'http://119.3.15.54/vcloud/open/media/record/snap/'  # 设备图片截取

VIDEO_URL = 'http://119.3.15.54/vcloud/open/media/record//handle/'  # 设备截取视频

PLAY_URL = 'http://119.3.15.54/vcloud/open/media/play/'  # 播放视频-获取视频流地址

STOP_PLAY_URL = 'http://119.3.15.54/vcloud/open/media/stopplay/'  # 停止播放流

PLAY_LIST_URL = 'http://119.3.15.54/vcloud/open/live/list/'  # 直播列表

SEARCH_VIDEO_URL = 'http://119.3.15.54/vcloud/open/media/record/list/'  # 查询视频录像

PLAY_VIDEO_URL = 'http://119.3.15.54/vcloud/open/media/record/playback/'  # 播放视频录像

STOP_VIDEO_URL = 'http://119.3.15.54/vcloud/open/media/record/stop_playback/'  # 暂停视频录像

TIME_OUT = 10  # 响应等待时间

ACCOUNT = 'szsl'  # 用户名

PASSWORD = 'e99a18c428cb38d5f260853678922e03'  # 密码

JSON_RESULT = {"Content-Type": "application/json;charset=UTF-8"}

FORM_RESULT = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}

APPEND_SLASH = False  # django自动处理url末尾是否加/

"""
访问时光云接口配置项 结束
"""

# ********************************************************************************

'''
访问水智能体接口配置项
'''
WATER_CONN_NUMBER = 3
WATER_TYPE_URL = "https://watergo.cn-east-2.myhuaweicloud.com/v1.0/b62c0a509c70428ba4ad489b814b4fd8/watergo/types"  # 检测类型接口

WATER_STREAM_URL = 'https://watergo.cn-east-2.myhuaweicloud.com/v1.0/b62c0a509c70428ba4ad489b814b4fd8/watergo/streams'  # 视频流接口

WATER_PROCESS_URL = 'https://watergo.cn-east-2.myhuaweicloud.com/v1.0/b62c0a509c70428ba4ad489b814b4fd8/watergo/process'  # 任务接口

WATER_MATCH_RESULT_URL = "https://watergo.cn-east-2.myhuaweicloud.com/v1.0/b62c0a509c70428ba4ad489b814b4fd8/watergo/match-results?"  # 匹配结果接口

NEW_ALARM_URL = "https://watergo.cn-east-2.myhuaweicloud.com/v1.0/b62c0a509c70428ba4ad489b814b4fd8/watergo/alarm-subscription"  # 创建告警上报方式

Project_id = 'b62c0a509c70428ba4ad489b814b4fd8'
Result_address = {"obs": {"bucket": "obs-swj", "path": "watergo/output/"}}
ALARM_ID = 'nDuyyD7y'

"""城管上报接口"""
SEND_URL = 'http://222.92.48.28:8015/gs-citywebservice/rest/CaseService/uploadcase'

# 日志管理
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), "adminy/logs/adminy.log"),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },

    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

