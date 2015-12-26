# -*- coding: utf-8 -*-

"""
Django settings for familyroot project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from familyroot import secrets
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
CSRF_COOKIE_HTTPONLY = False # Do some work to turn this on
X_FRAME_OPTIONS = 'DENY'

ALLOWED_HOSTS = [
                '.okkindred.com',  # Allow domain and subdomains
                'justinhui.pythonanywhere.com',
                ]

DOMAIN = 'https://www.okkindred.com'

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
    'rosetta',
    'gallery',
    'django.contrib.admin',
    'sign_up',
    #'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.FailedLoginMiddleware',
)

# Custom user model
AUTH_USER_MODEL = 'custom_user.User'

ROOT_URLCONF = 'familyroot.urls'

WSGI_APPLICATION = 'familyroot.wsgi.application'


#Django Axes config https://github.com/django-pci/django-axes
AXES_LOGIN_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 24
AXES_USERNAME_FORM_FIELD = "email"
AXES_PROTECTED_LOGINS = ('/accounts/login/', '/accounts/auth/')

#Email Configuration
EMAIL_SUBJECT_PREFIX = ''
EMAIL_USE_SSL = True
EMAIL_HOST = secrets.EMAIL_HOST
EMAIL_PORT = secrets.EMAIL_PORT
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL = 'info@okkindred.com'


#Rosetta
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_GOOGLE_TRANSLATE = True

#API Keys for external services
YANDEX_TRANSLATE_KEY = secrets.YANDEX_TRANSLATE_KEY
GOOGLE_API_KEY = secrets.GOOGLE_API_KEY
BING_MAPS_API_KEY = secrets.BING_MAPS_API_KEY


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
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = secrets.MEDIA_ROOT
MEDIA_ROOT_TEST = secrets.MEDIA_ROOT_TEST
#MEDIAFILES_DIRS = (os.path.join(BASE_DIR, 'media'),)

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

