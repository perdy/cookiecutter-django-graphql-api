from django.apps import AppConfig
from django.utils.translation import ugettext as _


default_app_config = 'core.apps.CoreApp'


class CoreApp(AppConfig):
    name = _('core')
    verbose_name = _('Core')

