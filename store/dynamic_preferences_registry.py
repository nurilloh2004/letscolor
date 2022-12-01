from dynamic_preferences.types import FloatPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry


currency = Section("currency")


@global_preferences_registry.register
class UsdCurrency(FloatPreference):
    section = currency
    name = "usd"
    default = 0.0
    required = False