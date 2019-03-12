"""
Django settings for loki project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import logging
import os

import requests
from logstash_formatter import LogstashFormatterV1

from .service_name import * # NOQA

STAGE = os.getenv('STAGE')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6bs=%8u-63g@_k8xodl-1@p9u6w=oo92ihtgsonerr00no8yy_'

ALLOWED_HOSTS = []

try:
    current_ip = requests.get(
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        timeout=1).content.decode('utf-8')
    ALLOWED_HOSTS.append(current_ip)
    logging.info(f'Append {current_ip} into ALLOWED_HOSTS')
except requests.ConnectionError as e:
    logging.info('Fail to get EC2 meta data with exception %s', e)

# Application definition

INSTALLED_APPS = [
    'cacheops_stats.apps.CacheopsStatsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cacheops',
    'corsheaders',
    'drf_yasg',
    'rest_framework',
]

MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',
    'main.middlewares.LogAnnotationMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': PROJECT_CODE,
        'USER': 'root',
        'PASSWORD': 'monkfish',
        'HOST': os.getenv('DB_HOST'),
        'POST': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = f'/{SERVICE_NAME}/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('CACHE_REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
        },
        'KEY_PREFIX': PROJECT_CODE
    },
}

# Cacheops
CACHEOPS_REDIS = os.getenv("CACHE_REDIS_URL")
CACHEOPS_PREFIX = lambda _: f'{PROJECT_NAME}.cacheops.'
CACHEOPS_DEFAULTS = {'timeout': 60 * 60}

CACHEOPS = {}

# django rest framework
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'PAGE_SIZE': 10,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'VERSION_PARAM': 'version',
}

# Loogging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logstash': {
            '()': LogstashFormatterV1
        },
        'simple': {
            'format':
            '[%(asctime)-15s][%(levelname)-5s][%(pathname)s %(module)s.%(funcName)s#%(lineno)d] %(message)s'
        },
    },
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
        'annotation': {
            '()': 'main.utils.loggers.AnnotationLogFilter'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/loki/service.log',
            'when': 'W3',
            'backupCount': 7,
            'formatter': 'simple'
        },
        'console': {
            'level': 'INFO',
            'filters': ['request_id', 'annotation'],
            'class': 'logging.StreamHandler',
            'formatter': 'logstash'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['file', 'console'],
            'propagate': True
        }
    }
}
