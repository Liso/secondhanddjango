"""
Django settings for secondhanddjango project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import urlparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w=&rmm%b#1=pd0753it0mnwli0@z46^qx9#x2=-6fis7v&ma&s'

SCRAPINGHUB_KEY = os.environ.get('SCRAPINGHUB_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not os.environ.get('PROD')

ALLOWED_HOSTS = [
'*'
]

ADMINS = (('Kevin Chen', 'yuechen1989@gmail.com'))
MANAGERS = (('Kevin Chen', 'yuechen1989@gmail.com'))

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'listing',
    'customers',
    'rest_framework',
    'djcelery',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.weibo.WeiboOAuth2',
   'social.backends.weixin.WeixinOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_WEIBO_KEY = os.environ.get('SOCIAL_AUTH_WEIBO_KEY')
SOCIAL_AUTH_WEIBO_SECRET = os.environ.get('SOCIAL_AUTH_WEIBO_SECRET')
SOCIAL_AUTH_WEIBO_DOMAIN_AS_USERNAME = True

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
)

ROOT_URLCONF = 'secondhanddjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'secondhanddjango.context_processors.prod',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
    ),
    'PAGE_SIZE': 10
}

WSGI_APPLICATION = 'secondhanddjango.wsgi.application'

if DEBUG:
    BROKER_URL = "amqp://admin:1234@localhost:5672/myvhost"
else:
    BROKER_URL = "amqp://zewdiccp:eC8HRQz7Zx4RBa_wGJ3my6HqOEQobJ53@wildboar.rmq.cloudamqp.com/zewdiccp"

BROKER_POOL_LIMIT = 3

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if DEBUG:
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
    }
  }
else:
  #DATABASES = {
  #  'default': {
  #      'ENGINE': 'django.db.backends.sqlite3',
  #      'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  #  }
  #}
  # Register database schemes in URLs.
  urlparse.uses_netloc.append('mysql')

  try:
   # Check to make sure DATABASES is set in settings.py file.
   # If not default to {}
    if 'DATABASES' not in locals():
        DATABASES = {}

    if 'DATABASE_URL' in os.environ:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        # Ensure default database exists.
        DATABASES['default'] = DATABASES.get('default', {})
        # Update with environment configuration.
        DATABASES['default'].update({
            'NAME': url.path[1:],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })

        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
  except Exception:
    print 'Unexpected error:', sys.exc_info()

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

CELERY_TIMEZONE = TIME_ZONE

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
LOGIN_URL = 'admin:login'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

ROLLBAR = {
    'access_token': 'c5f7e0a0e52b4cbb8b1ec241e782af5b',
    'environment': 'development' if DEBUG else 'production',
    'branch': 'master',
    'root': BASE_DIR,
}
