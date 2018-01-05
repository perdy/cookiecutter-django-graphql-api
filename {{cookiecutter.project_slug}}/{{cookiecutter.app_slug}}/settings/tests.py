"""
Tests settings
"""

from {{ cookiecutter.app_slug }}.settings import Development

__all__ = ['UnitTests']


class UnitTests(Development):
    pass
