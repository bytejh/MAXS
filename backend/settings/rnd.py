from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "rnd.datamarketing.kr",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://rnd.datamarketing.kr:8080",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mnsystem_rnd',
        'USER': 'themagnet',
        'PASSWORD': 'Bytejh2024!',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

CSRF_TRUSTED_ORIGINS = [
    "http://rnd.datamarketing.kr:8080",
    "https://rnd.datamarketing.kr",
    "http://localhost",
    "http://127.0.0.1"
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}


STATIC_ROOT = BASE_DIR / 'staticfiles_dev'
MEDIA_ROOT = BASE_DIR / 'mediafiles_dev'

SECURE_SSL_REDIRECT = False
CORS_ALLOW_CREDENTIALS = True
