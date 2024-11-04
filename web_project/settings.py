"""

Django's settings for web_project project.

Generated by 'django-admin startproject' using Django 5.1.1.


For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = "django-insecure-50g5np+4r3^wh1#stiw!@+wk5maiot-#&2)*j45_4@cl+3hhf8"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "txtencoder.apps.TxtencoderConfig",  
    "file_encoder.apps.FileEncoderConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'forum',
    'site_nav.apps.SiteNavConfig',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'site_nav.middleware.auth.InfoMiddleware',
    'site_nav.middleware.auth.LoginMiddleware',
    'site_nav.middleware.auth.AdminMiddleware',
    'site_nav.middleware.auth.UserMiddleware',
]
INTERNAL_IPS = [
    "127.0.0.1",
]

# React 应用运行的地址
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
ROOT_URLCONF = "web_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "web_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'forum',
        'USER': 'root',
        'PASSWORD': 'sher',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# 引用位于 STATIC_ROOT 中的静态文件时要使用的 URL
STATIC_URL = "static/"

# `python manage.py collectstatic` 将收集静态文件进行部署的目录的绝对路径
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# 将查找存储在 STATICFILES_DIRS 配置中的文件（使用 django.contrib.staticfiles.finders.FileSystemFinder）
# 和每个应用程序的 static 子目录中的文件（使用 django.contrib.staticfiles.finders.AppDirectoriesFinder）。
# 如果存在多个同名文件，将使用第一个找到的文件。
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
