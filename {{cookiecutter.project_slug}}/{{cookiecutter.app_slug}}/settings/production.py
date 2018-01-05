"""
Production settings
"""
import os

from {{ cookiecutter.app_slug }}.settings.base import Base

__all__ = ['Production']


class Production(Base):
    DEBUG = False

    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DB_DEFAULT_NAME'),
            'HOST': os.environ.get('DB_DEFAULT_HOST'),
            'PORT': os.environ.get('DB_DEFAULT_PORT'),
            'USER': os.environ.get('DB_DEFAULT_USER'),
            'PASSWORD': os.environ.get('DB_DEFAULT_PASSWORD'),
        },
    }

    # Check providers for django-status
    HEALTH_CHECK_PROVIDERS = {
        'health': (
            ('ping', 'health_check.providers.health.ping', None, None),
            ('databases', 'health_check.providers.django.health.databases', None, None),
        ),
    }

    CLINNER_DEFAULT_ARGS = {
        'runserver': '0.0.0.0:8000',
        'uwsgi': '--ini uwsgi.ini',
        'unit_tests': '--no-input',
    }

    @classmethod
    def pre_setup(cls):
        super(Production, cls).pre_setup()

        cls.REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.TokenAuthentication',
            ),
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',
            )
        }

        cls.REQUEST_LOGGING_EXCLUDE[''] += (r'{}'.format(cls.STATIC_URL),)

        # Disable logging
        cls.LOGGING['handlers']['console']['class'] = 'logging.NullHandler'
