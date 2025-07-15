# -*- coding: utf-8 -*-

"""
Django settings for okkindred project.

"""
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from okkindred import secrets
SECRET_KEY = secrets.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

# SSL Config
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600 # Increase this for production
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

CSRF_FAILURE_VIEW = 'okkindred.views.csrf_failure'
DEFAULT_AUTO_FIELD='django.db.models.AutoField'

ALLOWED_HOSTS = secrets.ALLOWED_HOSTS
INTERNAL_IPS = secrets.INTERNAL_IPS

DOMAIN = secrets.DOMAIN

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'custom_user',
    'family_tree',
    'axes',
    'emailer',
    'email_confirmation',
    'gallery',
    'django.contrib.admin',
    'sign_up',
    'corsheaders',
    'rest_framework',
    'django_rest_passwordreset',
    'rest_framework_simplejwt.token_blacklist',
    'person_api',
    'relation_api',
    'auth_api',
    'invite_email_api',
    'image_api',
    'profile_image_api',
    'gallery_api',
    'image_tagging_api',
    'message_queue',
    'suggested_image_tagging',
    'facial_recognition',
    'reversion',
    'chinese_relation_name',
)

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
)

# Custom user model
AUTH_USER_MODEL = 'custom_user.User'

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'okkindred.urls'

WSGI_APPLICATION = 'okkindred.wsgi.application'


#Django Axes config https://github.com/django-pci/django-axes
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 24
AXES_PROTECTED_LOGINS = ('/accounts/login/', '/accounts/auth/')
AXES_SENSITIVE_PARAMETERS = []

# PythonAnywhere behind load balancer https://github.com/un33k/django-ipware
# Log correct ip address to lockout multiple incorrect login attempts
IPWARE_META_PRECEDENCE_ORDER = (
    'HTTP_X_REAL_IP',
)


# ensure lockouts don't happen during tests
AXES_IP_WHITELIST = ['127.0.0.1']
AXES_NEVER_LOCKOUT_WHITELIST = True
AXES_IP_BLACKLIST = ['188.138.188.34', '5.61.51.32', '5.61.51.31', '185.17.149.137']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

AXES_CACHE = 'axes_cache'


#Email Configuration
EMAIL_SUBJECT_PREFIX = ''
EMAIL_USE_SSL = True
EMAIL_HOST = secrets.EMAIL_HOST
EMAIL_PORT = secrets.EMAIL_PORT
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = secrets.DEFAULT_FROM_EMAIL

ADMINS = secrets.ADMINS


#API Keys for external services
GOOGLE_API_KEY = secrets.GOOGLE_API_KEY
MAP_BOX_TOKEN = secrets.MAP_BOX_TOKEN

DATABASES = secrets.DATABASES

#SQLite Database for testing
import sys
if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'


#http://stackoverflow.com/questions/7728977/django-how-to-add-chinese-support-to-the-application
LANGUAGES = (

    ('en', _('English')),
    ('zh-tw', _('Traditional Chinese')),
    ('zh-cn', _('Simplified Chinese')),
    ('pl', _('Polish')),
    ('fi', _('Finnish')),
    ('fr', _('French')),

)


USE_I18N = True

USE_L10N = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")


MEDIA_URL = secrets.MEDIA_URL
MEDIA_ROOT = secrets.MEDIA_ROOT
MEDIA_ROOT_TEST = secrets.MEDIA_ROOT_TEST
MEDIA_URL_TEST = secrets.MEDIA_URL_TEST

AWS_STORAGE_BUCKET_NAME = secrets.AWS_STORAGE_BUCKET_NAME
AWS_STORAGE_BUCKET_NAME_TEST = secrets.AWS_STORAGE_BUCKET_NAME_TEST


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Rest framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
        'user': '2000/day'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

CORS_ALLOW_ALL_ORIGINS = secrets.CORS_ALLOW_ALL_ORIGINS
CORS_ALLOWED_ORIGINS = secrets.CORS_ALLOWED_ORIGINS

# JWT token for rest framework
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1000),

    'SLIDING_TOKEN_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1000),
}

# Password reset token expiry time in hours
DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 24

FACE_RECOG_BATCH_SIZE = 5
FACE_RECOG_MESSAGE_CHECK_INTERVAL_SECONDS = 3
FACE_RECOG_RESIZE_TAG_TEMP_DIR = secrets.FACE_RECOG_RESIZE_TAG_TEMP_DIR
FACE_RECOG_IMAGE_FACE_DETECT_TEMP_DIR = secrets.FACE_RECOG_IMAGE_FACE_DETECT_TEMP_DIR
FACE_RECOG_TRAIN_TEMP_DIR = secrets.FACE_RECOG_TRAIN_TEMP_DIR

FACE_RECOG_RESIZE_TAG_TEST_DIR = secrets.FACE_RECOG_RESIZE_TAG_TEST_DIR
FACE_RECOG_IMAGE_FACE_DETECT_TEST_DIR = secrets.FACE_RECOG_IMAGE_FACE_DETECT_TEST_DIR
FACE_RECOG_TRAIN_TEST_DIR = secrets.FACE_RECOG_TRAIN_TEST_DIR

