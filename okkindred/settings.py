# -*- coding: utf-8 -*-

"""
Django settings for okkindred project.

"""
from django.utils.translation import ugettext_lazy as _

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
    'debug_toolbar',
    'corsheaders',
    'rest_framework',
    'django_rest_passwordreset',
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
)

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
AXES_LOGIN_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 24
AXES_PROTECTED_LOGINS = ('/accounts/login/', '/accounts/auth/')

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
BING_MAPS_API_KEY = secrets.BING_MAPS_API_KEY
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

AWS_STORAGE_BUCKET_NAME = secrets.AWS_STORAGE_BUCKET_NAME


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

CORS_ORIGIN_ALLOW_ALL = secrets.CORS_ORIGIN_ALLOW_ALL
CORS_ORIGIN_WHITELIST = secrets.CORS_ORIGIN_WHITELIST

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

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

def show_toolbar(request):
    return DEBUG

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}

