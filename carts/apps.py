from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CartsConfig(AppConfig):
    name = 'carts'
    verbose_name = _('Carts')
