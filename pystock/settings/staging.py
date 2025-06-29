"""
Django STAGING settings for pystock project.
"""
from pystock.settings.base import env


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'local_pystock',
        'USER': env('DATABASE_USERNAME'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
