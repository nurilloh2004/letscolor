from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import greatkart.context_processors

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bcpmz7v*+b^252wpj@)d321(&udgp&633+s$p%wzqs7xg$oj1('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # General use templates & template tags (should appear first)
    'adminlte3',
    # Optional: Django admin theme (must be before django.contrib.admin)
    'adminlte3_theme',
    'django.contrib.admin',
    'django.contrib.auth',
    'dynamic_preferences',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rosetta',
    'parler',
    'accounts',
    'carts.apps.CartsConfig',
    'category.apps.CategoryConfig',
    'main.apps.MainConfig',
    'orders.apps.OrdersConfig',
    'store.apps.StoreConfig',

    'ckeditor',
    'ckeditor_uploader',
    'admin_honeypot',
    'storages',
    "mptt",

    "paycomuz",
    "clickuz",
    "rest_framework",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # default language
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'greatkart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'dynamic_preferences.processors.global_preferences',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Context for category
                'category.context_processors.menu_links',
                'category.context_processors.brands',
                'carts.context_processors.counter',
                'main.context_processors.menu_footer'
                # 'greatkart.context_processors.current_lang_path',
            ],
            'libraries': {
                'current_lang': 'greatkart.templatetags.current_lang',
                'reverse_lang': 'greatkart.templatetags.reverse_lang',
                'prettify_price': 'greatkart.templatetags.prettify_price',
                 }
        },
    },
]

WSGI_APPLICATION = 'greatkart.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'letscolor',
#         'USER': 'postgres',
#         'PASSWORD': 'datasite2022',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False
# For ckeditor
CKEDITOR_UPLOAD_PATH = "static/uploads/"
CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "greatkart", "static"),
]

# media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# django messages
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# SMTP configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'howareyouxan@gmail.com'
EMAIL_HOST_PASSWORD = '712007amirxan'
EMAIL_USE_TLS = True

# Parler
LANGUAGES = [
    ('ru', "ru"),
    ('uz', "uz"),
    ('en', "en"),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

PARLER_LANGUAGES = {
    None: (
        {'code': 'ru', },
        {'code': 'uz', },
        {'code': 'en', },
    ),
    'default': {
        'fallbacks': ['ru'],  # defaults to PARLER_DEFAULT_LANGUAGE_CODE
        'hide_untranslated': False,  # the default; let .active_translations() return fallbacks too.
    }
}

# Rosetta
ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'

ROSETTA_ACCESS_CONTROL_FUNCTION = "greatkart.settings.has_rosetta_access"


def has_rosetta_access(user):
    return user.is_superuser


PAYCOM_SETTINGS = {
    "KASSA_ID": "6184d62564198587b8943b03",
    "TOKEN": "6184d62564198587b8943b03",
    "SECRET_KEY": "#84uSW2G94NdG&Qkq2rUP8no&Gdn@P7K8Fz5",
    "ACCOUNTS": {
        "KEY": "order_id"
    }
}


CLICK_SETTINGS = {
    "service_id": "19585",
    "merchant_id": "14087",
    "secret_key": "C9ChF05CKs",
    "merchant_user_id": "22339"
}

# To Authentication

AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),
)