from .base import *  # noqa: F401,F403

STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "mail_admins": {
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "level": "ERROR",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}
