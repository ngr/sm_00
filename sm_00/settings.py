"""
Django settings for sm_00 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_ROOT = os.path.abspath(PROJECT_PATH)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+c*fyf4&xr@y7jthl$-yd1eo-%-&0=8qu#-=u3_i$=+ply59e='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.static",
        "django.core.context_processors.tz",
        "django.contrib.messages.context_processors.messages",
        'django.core.context_processors.request',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'slave',
    'skill',
    'task',
    'area',
    'item',
    'sm_00',
    'rest_framework',
    'oauth2_provider',
    'corsheaders',

)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
#    'talk.middleware.RequireLoginMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'sm_00.disable_csrf.DisableCSRF',
)
CORS_ORIGIN_ALLOW_ALL = True #FIXME
CORS_ORIGIN_WHITELIST = (
        'google.com',
        'fe.slave.center',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/django/logs/django-debug.log',
            'formatter': 'verbose'
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/django/logs/django-info.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': ['file_info'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}



AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    # Uncomment following if you want to access the admin
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
#    'DEFAULT_AUTHENTICATION_CLASSES': (
#        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
#    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    
} 
OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}


#LOGIN_REQUIRED_URLS = (
#    r'/talk/(.*)$',  # TODO interpret this regex.
#)
#LOGIN_REQUIRED_URLS_EXCEPTIONS = (
#    r'/login(.*)$',
#    r'/logout(.*)$',
#    r'/staff(.*)$',
#)


ROOT_URLCONF = 'sm_00.urls'

WSGI_APPLICATION = 'sm_00.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'old': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj_sm_00',
        'HOST': '127.0.0.1',
        'USER': 'dj_dbuser',
        'PASSWORD': 'P@ssw0rd',
        'PORT': '3306',
    },
    'db_task': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj_sm_01',
        'HOST': '127.0.0.1',
        'USER': 'dj_dbuser',
        'PASSWORD': 'P@ssw0rd',
        'PORT': '3306',
    },
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dj_sm_00',
        'HOST': 'rds-sm-00.cjlhgo3mq7ui.us-west-2.rds.amazonaws.com',
        'USER': 'dj_dbuser',
        'PASSWORD': 'P@ssw0rd',
        'PORT': '3306',
    },
}

#DATABASE_ROUTERS = ['task.dbRouter.AppSpecificDBRouter']

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
#print(STATIC_ROOT)
STATICFILES_DIRS = (
    '/var/django/sm_00/shared_static',
)

# CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Authorization and Authentication
LOGIN_REDIRECT_URL = '/'
