import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

from .utils import strtobool

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-$f_u#a1!k0rg(h*ftp#0!8_g1@s2+iotgl&h%$m#mmr$&&n%hm",
)

DEBUG = strtobool(os.getenv("DEBUG", "n"))

ALLOWED_HOSTS = [s.strip() for s in os.getenv("ALLOWED_HOSTS", "").split(",") if s]

# Application definition

INSTALLED_APPS = [
    "manage_currency",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pipeline",
    "django_bootstrap5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "event_administrator.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "event_administrator.wsgi.application"

# Database

DATABASES = {
    "default": dj_database_url.config(default="sqlite:///db.sqlite3"),
}

# Password validation

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


LANGUAGE_CODE = "ja"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
]

# User-uploaded files

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = EMAIL_PORT == 578
EMAIL_USE_SSL = EMAIL_PORT == 465

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "no-reply@example.com")

# Logging

SERVER_EMAIL = os.getenv("SERVER_EMAIL", DEFAULT_FROM_EMAIL)

ADMINS = list(
    zip(
        os.getenv("ADMIN_NAMES", "").split(","),
        os.getenv("ADMIN_EMAILS", "").split(","),
    )
)

# django-pipeline (https://django-pipeline.readthedocs.io/en/stable/configuration.html)

PIPELINE = {
    "COMPILERS": [
        "pipeline.compilers.sass.SASSCompiler",
    ],
    "SASS_BINARY": "npx sass",
    "SASS_ARGUMENTS": "--style=compressed",
    "CSS_COMPRESSOR": None,  # already compressed by sass compiler
    "JS_COMPRESSOR": "pipeline.compressors.uglifyjs.UglifyJSCompressor",
    "UGLIFYJS_BINARY": "npx terser",
    "UGLIFYJS_ARGUMENTS": "--compress --mangle",
    "STYLESHEETS": {
        "base": {
            "source_filenames": [
                "manage_currency/css/base.scss",
            ],
            "output_filename": "manage_currency/css/base.css",
        },
        "top": {
            "source_filenames": [
                "manage_currency/css/top.scss",
            ],
            "output_filename": "manage_currency/css/top.css",
        },
        "product-list": {
            "source_filenames": [
                "manage_currency/css/product-list.scss",
            ],
            "output_filename": "manage_currency/css/product-list.css",
        },
        "purchase": {
            "source_filenames": [
                "manage_currency/css/purchase.scss",
            ],
            "output_filename": "manage_currency/css/purchase.css",
        },
        "login": {
            "source_filenames": [
                "manage_currency/css/login.scss",
            ],
            "output_filename": "manage_currency/css/login.css",
        },
        "quiz": {
            "source_filenames": [
                "manage_currency/css/quiz.scss",
            ],
            "output_filename": "manage_currency/css/quiz.css",
        },
        "trade": {
            "source_filenames": [
                "manage_currency/css/trade.scss",
            ],
            "output_filename": "manage_currency/css/trade.css",
        },
        "trade-started": {
            "source_filenames": [
                "manage_currency/css/trade-started.scss",
            ],
            "output_filename": "manage_currency/css/trade-started.css",
        },
        "trade-finished": {
            "source_filenames": [
                "manage_currency/css/trade-finished.scss",
            ],
            "output_filename": "manage_currency/css/trade-finished.css",
        },
        "signup": {
            "source_filenames": [
                "manage_currency/css/signup.scss",
            ],
            "output_filename": "manage_currency/css/signup.css",
        },
    },
    "JAVASCRIPT": {},
}

AUTH_USER_MODEL = "manage_currency.Member"

LOGIN_URL = "/event/login/"
LOGIN_REDIRECT_URL = "/event/top/"
LOGOUT_REDIRECT_URL = LOGIN_URL
