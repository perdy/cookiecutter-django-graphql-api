"""
Development settings
"""
import os

from {{ cookiecutter.app_slug }}.settings.base import Base

__all__ = ['Development']


class Development(Base):
    DEBUG = True

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

    CLINNER_DEFAULT_ARGS = {
        'runserver': '0.0.0.0:8000',
        'uwsgi': '--ini uwsgi.ini',
        'unit_tests': '--no-input',
    }

    @classmethod
    def pre_setup(cls):
        super(Development, cls).pre_setup()

        cls.REST_FRAMEWORK = {
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.TokenAuthentication',
                'rest_framework.authentication.SessionAuthentication',
            ),
            'DEFAULT_RENDERER_CLASSES': (
                'rest_framework.renderers.JSONRenderer',
                'rest_framework.renderers.BrowsableAPIRenderer',
            )
        }

        os.environ['DJANGO_SECRET_KEY'] = os.environ.get('DJANGO_SECRET_KEY', '1234567890')

        cls.REQUEST_LOGGING_EXCLUDE[''] += (r'{}'.format(cls.STATIC_URL),)

        for handler, props in cls.LOGGING['handlers'].items():
            props['level'] = 'DEBUG'

        for logger, props in cls.LOGGING['loggers'].items():
            props['level'] = 'DEBUG'
