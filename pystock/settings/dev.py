"""
Django DEVELOPMENT settings for pystock project.
"""
from pystock.settings.base import *


ALLOWED_HOSTS = ['127.0.0.1']


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Email configuration

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
