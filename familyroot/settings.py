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

TEMPLATE_DEBUG = False

SSLIFY_DISABLE = False #Set this to true to run the unit tests!

ALLOWED_HOSTS = [
                '.okkindred.com',  # Allow domain and subdomains
                ]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
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
)

MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
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


#Rosetta
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
YANDEX_TRANSLATE_KEY  = secrets.YANDEX_TRANSLATE_KEY

#Doesn't work...
#ROSETTA_WSGI_AUTO_RELOAD = DEBUG

#SQLite Database for dev
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

DATABASES = secrets.DATABASES


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'


#http://stackoverflow.com/questions/7728977/django-how-to-add-chinese-support-to-the-application
LANGUAGES = (

    ('en', _('English')),
    ('zh-hk', _('Traditional Chinese')),
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
MEDIA_ROOT = '/home/justinhui/media/okkindred/'
#MEDIAFILES_DIRS = (os.path.join(BASE_DIR, 'media'),)

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	os.path.join(BASE_DIR, 'templates'),
)

