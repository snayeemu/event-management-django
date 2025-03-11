"""
Django settings for event_management project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import dj_database_url
import os 
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)rh$zh1udw$=d@w9kaj6qphwds#pk=5(in&r3#d$w5z56yx9#o"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com", "http://127.0.0.1:8000"]


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "events",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compressor",
    "debug_toolbar",
    "users",
    "core",
    "heroicons",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware', #add it exactly here
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

ROOT_URLCONF = "event_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["events/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "event_management.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "event_management",
#         "USER": "postgres",
#         "PASSWORD": "password",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

# Replace the SQLite DATABASES configuration with PostgreSQL:
DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://event_manager_db_ozcd_user:xVP6SwiFn4HFcdQZMQddPh0evHBWGdxC@dpg-cuqvlnq3esus739ti3u0-a.oregon-postgres.render.com/event_manager_db_ozcd',
        conn_max_age=600
    )
}




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

COMPRESS_ROOT = BASE_DIR / 'static'

COMPRESS_ENABLED = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',  # Default
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # Default
    'compressor.finders.CompressorFinder',  # Django Compressor
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_PORT = config("EMAIL_PORT", cast=int)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

FRONTEND_URL = "http://127.0.0.1:8000"
LOGIN_URL = "sign-in"