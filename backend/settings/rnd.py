from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "rnd.datamarketing.kr",
    "datamarketing.kr"
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://172.233.90.46:8080",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'staticfiles_dev'
MEDIA_ROOT = BASE_DIR / 'mediafiles_dev'

SECURE_SSL_REDIRECT = False

