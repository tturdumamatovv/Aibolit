"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
import datetime
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(' ')

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Installed
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    # Created
    'apps.authentication',
    'apps.medicine',
    'apps.order',

]

AUTH_USER_MODEL = "authentication.User"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = "*"

# CSRF_TRUSTED_ORIGINS = ['https://tatadev.pro/', 'https://www.tatadev.pro/']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # AutoSchema для drf-spectacular
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7)
}

DEFAULT_PROFILE_PICTURE_URL = MEDIA_URL + 'profile_pictures/default-user.jpg'


SPECTACULAR_SETTINGS = {
    "TITLE": "Aibolit OpenAPI",
    "DESCRIPTION": "Описание нашего API в разработке...",
    'COMPONENT_SPLIT_REQUEST': True,
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SERVE_PERMISSIONS": ("rest_framework.permissions.IsAdminUser", ),
    "SERVE_AUTHENTICATION": ('rest_framework.authentication.SessionAuthentication',
                             'rest_framework.authentication.BasicAuthentication'),
    "PREPROCESSING_HOOKS": ("apps.openapi.preprocessors.get_urls_preprocessor",),
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",  # 'none' | 'list' | 'full'
    },
    "GENERATE_UNIQUE_PARAMETER_NAMES": True,

    # "ENUM_NAME_OVERRIDES": {
    #     "RatingsEnum": "apps.autoanswers.models.RatingChoices",
    #     "CountMonthsEnum": "api.billing.serializers.PeriodChoices",
    # },
    "SERVE_PERMISSIONS": ("rest_framework.permissions.AllowAny",)
}


SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_DEFAULT_THEME = 'simpleui.css'
SIMPLEUI_INDEX = '#'
SIMPLEUI_LOGO = '/static/icons/LOGO.png'
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menus': [
        {
            'name': 'Пользователи и адреса',
            'icon': 'fa fa-book',
            'models': [
                {
                    'name': 'Пользователь',
                    'icon': 'fa fa-user',
                    'url': '/admin/authentication/user/'
                },
                {
                    'name': 'Адреса пользователей',
                    'icon': 'fa fa-home',
                    'url': '/admin/authentication/useraddress/'
                },
            ]
        },
        {
            'name': 'Продукты и категории',
            'icon': 'fa fa-heartbeat',
            'models': [
                {
                    'name': 'Продукты',
                    'icon': 'fa fa-medkit',
                    'url': '/admin/medicine/product/'
                },
                {
                    'name': 'Категории',
                    'icon': 'fa fa-list-alt',
                    'url': '/admin/medicine/category/'
                },
            ]
        },
        {
            'name': 'Заказы',
            'icon': 'fa fa-shopping-cart',
            'models': [
                {
                    'name': 'Заказы',
                    'icon': 'fa fa-shopping-cart',
                    'url': '/admin/order/order/'
                },
                {
                    'name': 'Элементы заказа',
                    'icon': 'fa fa-shopping-basket',
                    'url': '/admin/order/orderitem/'
                },
            ]
        },
        {
            'name': 'Настройки',
            'icon': 'fa fa-cog',
            'models': [
                {
                    'name': 'Бонусы',
                    'icon': 'fa fa-gift',
                    'url': '/admin/order/bonusconfiguration/'
                },
                {
                    'name': 'Доставка',
                    'icon': 'fa fa-shipping-fast',
                    'url': '/admin/order/deliveryconfiguration/'
                },
            ]
        },
        # {
        #
        #     'name': 'Страницы',
        #     'icon': 'fa fa-book',
        #     'models': [
        #         {
        #             'name': 'О нас',
        #             'icon': 'fa fa-info-circle',
        #             'models': [
        #                 {
        #                     'name': 'Страница О нас',
        #                     'icon': 'fa fa-file-text',
        #                     'url': '/admin/about_us/aboutpage/'
        #                 },
        #                 {
        #                     'name': 'Блоки',
        #                     'icon': 'fa fa-cubes',
        #                     'url': '/admin/about_us/contentblock/'
        #                 },
        #
        #             ]
        #         },
        #         {
        #             'name': 'Портфолио',
        #             'icon': 'fa fa-folder',
        #             'models': [
        #                 {
        #                     'name': 'Страница Портфолио',
        #                     'icon': 'fa fa-file-text',
        #                     'url': '/admin/portfolio/portfoliopage/'
        #                 },
        #                 {
        #                     'name': 'Направление',
        #                     'icon': 'fa fa-arrows',
        #                     'url': '/admin/portfolio/portfolioduration/'
        #                 },
        #                 {
        #                     'name': 'Проекты',
        #                     'icon': 'fa fa-industry',
        #                     'url': '/admin/portfolio/portfolioproject/'
        #                 },
        #             ]
        #         },
        #         {
        #             'name': 'Услуги',
        #             'icon': 'fa fa-user',
        #             'models': [
        #                 {
        #                     'name': 'Страница Услуг',
        #                     'icon': 'fa fa-file-text',
        #                     'url': '/admin/services/servicepage/'
        #                 },
        #                 {
        #                     'name': 'Услуги',
        #                     'icon': 'fa fa-cube',
        #                     'url': '/admin/services/service/'
        #                 },
        #                 {
        #                     'name': 'Блоки сервисов',
        #                     'icon': 'fa fa-cubes',
        #                     'url': '/admin/services/contentblock/'
        #                 },
        #
        #             ]
        #         },
        #         {
        #             'name': 'Контакты',
        #             'icon': 'fa fa-address-book',
        #             'url': '/admin/contacts/contact/'
        #         },
        #
        #
        #
        #     ]
        # },
        # {
        #     'name': 'Заявки',
        #     'icon': 'fa fa-list',
        #     'url': '/admin/contacts/application/'
        # },

    ]
}
