"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
import dj_database_url
import environ





# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#_yt)w^e3=hu^us1c*n6y(%5foqx=wg=tik%te%d=0$&w+)qgp'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'chatgpt-mqox.onrender.com']


# Application definition

INSTALLED_APPS = [
    # 'accounts.apps.AccountsConfig',  # 追加
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'story_app',
    'storages',
    'accounts',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    # この行を追加

]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


default_dburl = "sqlite:///" + str(BASE_DIR / "db.sqlite3")
DATABASES = {'default': dj_database_url.config(default=default_dburl)}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
DEBUG = False # デプロイ時、Falseに修正

if DEBUG==True:

    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'story_app/static/story_app'),)
    STATIC_ROOT = os.path.join(BASE_DIR, 'story_app/staticfiles')   
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
            'django.server': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }

else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'story_app/static/story_app'),)
    STATIC_ROOT = os.path.join(BASE_DIR, 'story_app/staticfiles')    
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = 'myback3'
    AWS_S3_REGION_NAME = 'ap-northeast-1'
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    from config.aws.conf import *




# 以下を追加

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

SUPERUSER_NAME = env("SUPERUSER_NAME")
SUPERUSER_EMAIL = env("SUPERUSER_EMAIL")
SUPERUSER_PASSWORD = env("SUPERUSER_PASSWORD")


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'story_app:index'
LOGOUT_REDIRECT_URL = 'story_app:home'

AUTH_USER_MODEL = 'accounts.CustomUser'

