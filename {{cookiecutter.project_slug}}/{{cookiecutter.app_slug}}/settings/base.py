"""
Django settings.
"""

import os

from configurations import Configuration, values

__all__ = ['Base']


class LoggingMixin:
    """
    Logging configuration.
    """
    LOG_DIR = os.path.abspath(os.environ.get('DJANGO_APP_LOG_DIR', '/srv/apps/{{ cookiecutter.project_slug }}/logs'))

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'plain': {
                'format': '[%(asctime)s.%(msecs)dZ] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'plain'
            },
            'root_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'root.log'),
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'base_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'base.log'),
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'runserver_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'runserver.log'),
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'request_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'request.log'),
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'security_file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOG_DIR, 'security.log'),
                'formatter': 'plain',
                'when': 'midnight',
                'backupCount': 30,
                'utc': True
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True,
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'root_file', 'mail_admins'],
                'level': 'INFO',
                'propagate': True,
            },
            'recipes': {
                'handlers': ['console', 'base_file', 'mail_admins'],
                'level': 'INFO',
                'propagate': False,
            },
            '{{ cookiecutter.app_slug }}': {
                'handlers': ['console', 'base_file', 'mail_admins'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.server': {
                'handlers': ['console', 'runserver_file'],
                'level': 'INFO',
                'propagate': True,
            },
            'recipes.middleware': {
                'handlers': ['console', 'request_file', 'mail_admins'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.security': {
                'handlers': ['console', 'security_file', 'mail_admins'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }


class RESTFrameworkMixin:
    REST_FRAMEWORK = {}


class Base(LoggingMixin, RESTFrameworkMixin, Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['*']
    ADMINS = values.SingleNestedTupleValue((
        ('Souft', 'souft@souft.es'),
    ))

    # Application definition

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Project apps
        '{{ cookiecutter.app_slug }}',
        'core',
        'recipes',
        # GraphQL
        'graphene_django',
        'django_filters',
        # System utilities
        'redis_cache',
        'health_check',
        # Django fields
        'imagekit',
        # REST framework
        'rest_framework',
        'rest_framework.authtoken',
        # Django utilities
        'django_extensions',
        'django_cleanup',
    )

    MIDDLEWARE = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
    )

    ROOT_URLCONF = '{{ cookiecutter.app_slug }}.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = '{{ cookiecutter.app_slug }}.wsgi.application'

    # Database
    DATABASES = {
        'default': {},
    }

    # Cache
    DEFAULT_CACHE_TIMEOUT = 60 * 15
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }

    # Internationalization
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'assets'))  # Copy files to ./{{ cookiecutter.project_slug }}/assets
    STATICFILES_DIRS = [
    ]

    # Media files (Upload by user)
    MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media'))  # Copy media files to ./{{ cookiecutter.project_slug }}/media
    MEDIA_URL = '/media/'

    # Static finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        # other finders..
    )
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    # Regex expresions to exclude from logging at middleware
    REQUEST_LOGGING_EXCLUDE = {
        '': (

        ),
        'admin': (
            r'.*',
        ),
        'health_check': (
            r'.*',
        )
    }

    DEFAULT_RESPONSE_HEADERS = {
        'Link': (
            '<https://docs.sequoia.piksel.com/concepts/api/spec.html>;rel="profile"',
        ),
        'Cache-Control': (
            'no-cache',
        ),
    }

    HEALTH_CHECK_PROVIDERS = {
        'health': (
            ('ping', 'health_check.providers.health.ping', None, None),
            ('databases', 'health_check.providers.django.health.databases', None, None),
        ),
        'stats': (
            ('databases', 'health_check.providers.django.stats.databases', None, None),
            ('code', 'health_check.providers.stats.code', None, None),
        )
    }
