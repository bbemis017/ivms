"""
Django settings for simpledjango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '',                      # Or path to database file if using sqlite3.
            'USER': 'd066bdb7644ff450396c85bf550e22433',                      # Not used with sqlite3.
            'PASSWORD': 'p5141a9f751384e25bdee91f7c35826b1',                  # Not used with sqlite3.
            'HOST': '192.155.243.18',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': 5433,                      # Set to empty string for default. Not used with sqlite3.
            }
        }

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+we06q!vu7)e-01^o@_4$*2$q$zh2u9=k08yfzhp0@^iws!gto'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        #our apps
        'accounts',
        'chat',
        )

MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        )


TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [ os.path.join(BASE_DIR,'static')
                ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    ],
                'debug' : DEBUG,
                },
            },
        ]

TEMPLATE_DIRS = [
        os.path.join(BASE_DIR,'static'),
        ]


ROOT_URLCONF = 'config.urls'


local = False
try:
    from local_settings import *
    local = True
    print "local env"
except ImportError:
    print "not local"
    WSGI_APPLICATION = 'config.wsgi.application'
    pass



# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if not local:
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Parse database configuration from $DATABASE_URL
if not local:
    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
        )



