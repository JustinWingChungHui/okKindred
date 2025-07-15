# -*- coding: utf-8 -*-

"""
An example secrets.py

Rename this file to secrets.py, fill in your keys/passwords etc and make sure it doesn't get checked into a public repository!

You will also need to set up AWS credentials in a separate file (e.g. ~/.aws/credentials):

[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET

[default]
region=us-east-1

"""

# Django Secret Key
SECRET_KEY = 'YOUR_DJANGO_KEY'

# Google API key to use geocoding service
GOOGLE_API_KEY = 'GOOGLEMAPS_API_KEY'

# Mapbox is used for any mapping and as a backup geocoding service
MAP_BOX_TOKEN = 'MAP_BOX_TOKEN'


# Email server set up to send out notification emails
EMAIL_HOST = 'SERVER_ADDRESS'
EMAIL_PORT = 465

EMAIL_HOST_USER = 'USERNAME'
EMAIL_HOST_PASSWORD = 'PASSWORD'
DEFAULT_FROM_EMAIL = 'info@okkindred.com'


# Database setup.  On PythonAnywhere, it is cheaper & easier to use MySQL.
# Remember to set up a separate database to run the automated tests
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'username$databasename',
         'USER': 'username',
         'PASSWORD': "databasepassword",
         'HOST': 'username.mysql.pythonanywhere-services.com',
         'TEST': {
             'NAME': 'username$test_databasename',
         },
    }
}

# Make sure the following directories exist
MEDIA_ROOT = '/home/USERNAME/media/okkindred/'
MEDIA_ROOT_TEST = '/home/USERNAME/media/test/'
MEDIA_URL = 'S3_OR_CLOUDFRONT_URL_WHERE_IMAGES_ARE_HOSTED'

ALLOWED_HOSTS = [
                '.okkindred.com',  # Allow domain and subdomains
                'USERNAME.pythonanywhere.com',
                'YOUR_CUSTOM_DOMAIN',
                ]

# Internal IP of your server
INTERNAL_IPS = ('11.11.111.111',)

# This is used in emails to provide hyperlinks to site
DOMAIN = 'https://YOUR_CUSTOM_DOMAIN'


# The AWS S3 bucket in which the images will be uploaded to
AWS_STORAGE_BUCKET_NAME = 'IMAGE_STORAGE_BUCKET_NAME'
AWS_STORAGE_BUCKET_NAME_TEST = 'TEST_IMAGE_STORAGE_BUCKET_NAME'

CORS_ALLOW_ALL_ORIGINS = False

# Address of UI
CORS_ALLOWED_ORIGINS = (
    'ui_domain.com',
)


FACE_RECOG_RESIZE_TAG_TEMP_DIR = '/home/USERNAME/media/facial_recognition_dev/resize_tags/'
FACE_RECOG_IMAGE_FACE_DETECT_TEMP_DIR = '/home/USERNAME/media/facial_recognition_dev/image_face_detect/'
FACE_RECOG_TRAIN_TEMP_DIR = '/home/USERNAME/media/facial_recognition_dev/train_face_recognition/'

FACE_RECOG_RESIZE_TAG_TEST_DIR = '/home/USERNAME/media/facial_recognition_dev/resize_tags/'
FACE_RECOG_IMAGE_FACE_DETECT_TEST_DIR = '/home/USERNAME/media/facial_recognition_dev/image_face_detect/'
FACE_RECOG_TRAIN_TEST_DIR = '/home/USERNAME/media/facial_recognition_dev/train_face_recognition/'
