"""
Django settings for django_docker_project project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*=!&u!lo3#+x81ensp^^ma5&edf9uqb7_cb&=ew!g8yx^f81e3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

try:
    load_dotenv(dotenv_path, verbose=True, override=True, encoding = 'utf_8')
except UserWarning:
    raise ImproperlyConfigured('.env file not found. Did you forget to add one?')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat', # `App` for `CELERY_BEAT`
    'django_docker_project',
    'travello',
    'flexbox_tutorial',
    'learn_celery_tutorial',
    'EmailApp',
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

ROOT_URLCONF = 'django_docker_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_docker_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path={}'.format(os.getenv('DEFAULT_DB_SCHEMA'))
        },
        'NAME': os.getenv('DEFAULT_DB_NAME'), #'telusko_web_backend',
        'USER': os.getenv('DEFAULT_DB_USER'), #'postgres',
        'PASSWORD': os.getenv('DEFAULT_DB_PASSWORD'), #'postgres',
        'HOST': os.getenv('DEFAULT_DB_HOST'), #'travello_db', # Service NAME in DOCKER-COMPOSE
        'PORT': os.getenv('DEFAULT_DB_PORT'), #'5432' # The port on which the PostgreSQL container is listening
        'TEST': {
            'NAME': 'travello_test',
            'ENGINE': 'django.db.backends.sqlite3',
        }


    }
}




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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('CACHE_LOCATION'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "E_Learniverse"
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(__file__), 'static'),
]

# CELERY Stuffs
#   default
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_TASK_DEFAULT_QUEUE = os.getenv('CELERY_TASK_DEFAULT_QUEUE')
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_TASK_ROUTES = ([
    ('learn_celery_tutorial.add_numbers', {'queue': 'custom_queue'}),
],)

CELERY_BEAT_SCHEDULE = {
    'number-counter-using-celery-beat': {
        'task': 'learn_celery_tutorial.number_counter_using_celery_beat',
        # 'schedule': crontab(minute='*/10'),
        'schedule': timedelta(seconds=10),
        'kwargs': {'number': 5},
        # 'args': (3, 7),  # Example numbers to add
        # 'kwargs': {'number1': 5, 'number2': 7},
    },
}


# MEDIA & STATIC STUFF
STATIC_ROOT = os.path.join(BASE_DIR,'assets')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR , 'media')

# Email Configurations
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# Port for sending e-mail.
EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS').upper() == 'TRUE'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')