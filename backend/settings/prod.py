from .base import *

DEBUG = False

ALLOWED_HOSTS = ['datamarketing.kr', 'www.datamarketing.kr', '172.233.90.46']

CORS_ALLOWED_ORIGINS = [
    "https://datamarketing.kr",
    "https://www.datamarketing.kr",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mnsystem',
        'USER': 'themagnet',
        'PASSWORD': 'Bytejh2024!',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'

SECURE_SSL_REDIRECT = True

