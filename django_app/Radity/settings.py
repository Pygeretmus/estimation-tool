import json
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR.parent / "docker" / ".env"
load_dotenv(dotenv_path=env_path)


def get_secret(key: str, default=None):
    return os.getenv(key, default)


SECRET_KEY = get_secret("SECRET_KEY")
DEBUG = get_secret("DEBUG") in ["True", "true", "TRUE"]

ALLOWED_HOSTS = json.loads(get_secret("ALLOWED_HOSTS", "[]"))
CSRF_TRUSTED_ORIGINS = json.loads(get_secret("CSRF_TRUSTED_ORIGINS", "[]"))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3-party apps
    "rest_framework",
    "drf_spectacular",
    # Local apps
    "estimation_tool",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Radity.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "Radity.wsgi.application"

DATABASE_NAME = get_secret("POSTGRES_DB")
if DATABASE_NAME:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DATABASE_NAME,
            "USER": get_secret("POSTGRES_USER"),
            "PASSWORD": get_secret("POSTGRES_PASSWORD"),
            "HOST": get_secret("DB_HOST"),
            "PORT": get_secret("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR / "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "Radity.exceptions.exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Radity API",
    "DESCRIPTION": "Estimation tool",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
