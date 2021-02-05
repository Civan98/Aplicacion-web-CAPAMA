from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['capamaappweb.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd94d6j212q36rl',
        'USER': 'vnbbycaoogxzuj',
        'PASSWORD': '15230dde06eedf9f95609eddd6bdc4f3ed65f81174f7a7b29caf2c98b75068c9',
        'HOST': 'ec2-3-232-148-66.compute-1.amazonaws.com',
        'DATABASE_PORT': '5432',
    }
}

STATICFILES_DIR = (BASE_DIR, 'static')
