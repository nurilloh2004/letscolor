from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StoreConfig(AppConfig):
    name = 'store'
    verbose_name = _('Store')
