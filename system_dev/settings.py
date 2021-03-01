"""
Django settings for system_dev project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from conf.simpleui_conf import *
import sys
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

from jinja2 import Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
#  pyecharts 模板，位于 pyecharts.render.templates 拷贝至刚新建的 templates_pyecharts 文件夹
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("{}/templates/templates_pyecharts".format(BASE_DIR)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%fm7s!v=nl)+lx96@#ws@es98x)8qs%n44@v%pd)2f4rd3wadb'

# SECURITY WARNING: don't run with debug turned on in production!
# todo: just for debug
DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'user_manage',
    'data_display',
    'test_install',
    'warning_manage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',     #设置跨域
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'system_dev.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'libraries': {
            #     'simpleui': 'simpleui.templatetags.simpletags',  # 添加位置
            # }
        },
    },
]

WSGI_APPLICATION = 'system_dev.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
	'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'tms1',
    'USER': 'root',
    'PASSWORD': '123456',
    'HOST': 'localhost',
    'PORT': '3306',
    },
}
# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.postgresql',
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'bgs',
#         'USER': 'postgres',
#         'PASSWORD': '123456',
#         'HOST': '192.168.13.14',
#         'PORT': '5432',
#     },
# }
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'user_manage.User'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'  #en-us

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]

# STATIC_ROOT = os.path.join(BASE_DIR, "real_static")


# 设置上传目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 设置前缀
MEDIA_URL = '/media/'

# 配置登录地址
# LOGIN_URL = '/login'

#设置跨域(一个导包三处配置)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True