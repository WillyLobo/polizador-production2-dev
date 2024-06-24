"""
Django settings for polizador project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import environ
import os
from pathlib import Path
from google.oauth2 import service_account

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# "Secret" Variables.
DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
DBHOST=env("DBHOST")
DBUSER=env("DBUSER")
DBNAME=env("DBNAME")
DBSECRET=env("DBPASSWORD")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

ALLOWED_HOSTS = [
	"www.willylobo.net.ar",
	"127.0.0.1"
	]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    "debug_toolbar",
    "django_select2",
    "ajax_datatable",
	"import_export",
    'easyaudit',
	"widget_tweaks",
	"extra_views",
	"django.forms",

    "carga",
	"secretariador",
    "fallout",
]

# Widget template override. Place "widgetX.html" into "templates/django/forms/widgets/"
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
	"whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
	'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'polizador.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
			BASE_DIR / "templates",
			BASE_DIR / "polizador/carga/templates",
            ],
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
TEMPLATES[0]['OPTIONS']['context_processors'].append("polizador.context_processors.imglinks")

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 3600
    }
}
SELECT2_CACHE_BACKEND = "select2"
SELECT2_THEME = "bootstrap-5"
WSGI_APPLICATION = 'polizador.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": DBHOST,
        "USER": DBUSER,
	    "PASSWORD":DBSECRET,
        "NAME":DBNAME,
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
LANGUAGE_CODE = 'es-AR'

DATETIME_FORMAT="%d-%B-%Y" # "Dia en Numeros" - "Nombre Completo del Mes" - "Número Completo del Año"

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True
USE_THOUSAND_SEPARATOR = True

# Cloud Storage

GS_CREDENTIALS = service_account.Credentials.from_service_account_file("polizador-production.json")
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'polizador-production-pdf'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirects after Authentication

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = "/home/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "static_files/static"
STATIC_FILES_DIRS = [
    BASE_DIR / "static_files",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
