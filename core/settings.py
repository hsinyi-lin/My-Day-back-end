"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '15i6)scshrob#x9*0$l)8l^g9m43_ty9jug!tu)md=j8&v9w!s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['myday.sytes.net', '127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account.apps.AccountConfig',
    'friend.apps.FriendConfig',
    'group.apps.GroupConfig',
    'note.apps.NoteConfig',
    'schedule.apps.ScheduleConfig',
    'temporary_group.apps.TemporaryGroupConfig',
    'timetable.apps.TimetableConfig',
    'user_profile.apps.UserProfileConfig',
    'vote.apps.VoteConfig',
    'api.apps.ApiConfig',
    'rest_framework',
    'bootstrap4',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MyDay',
        'USER': 'MyDay110504',
        'PASSWORD': '10656004',
        'HOST': 'mydaydb.cjadqiztqjax.ap-northeast-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DATE_FORMAT = 'Y-m-d'

DATETIME_FORMAT = 'Y-m-d H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main': {
            'format': '{asctime} >> {levelname}: {message}',
            'style': '{'
        },
        'simple': {
            'format': '{asctime}\t{message}',
            'style': '{'
        }
    },
    'handlers': {
        'my_day_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './logs/my_day.log',
            'formatter': 'main'
        },
        'django_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './logs/django.log',
            'formatter': 'main'
        },
        'message_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './logs/message.log',
            'formatter': 'main'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'my_day': {
            'handlers': ['my_day_log'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django': {
            'handlers': ['django_log', 'console'],
            'level': 'INFO',
            'propagate': True
        },
        'message': {
            'handlers': ['message_log'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
