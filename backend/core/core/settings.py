import datetime
from pathlib import Path
import structlog
from dotenv import load_dotenv
import os

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get(
    "SECRET_KEY", default="awdojawoidjq39ur89hfajsncz3827$$@#avHfalwm"
)
DEBUG = int(os.environ.get("DEBUG", default=0))
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="*").split(",")
CELERY_BROKER_URL = "redis://redis-qoovee/1"
CELERY_RESULTS_URL = "redis://redis-qoovee/1"
AUTH_USER_MODEL = "account.UserAccount"

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",
    "drf_spectacular",
    "django_structlog",
    "channels",
    "corsheaders",
    "django_prometheus",
    "whitenoise",
    "account",
    "collection",
    "museum",
    "messenger",
    "constructor",
    "core.celery.apps.CeleryConfig",
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://127.0.0.1:5173",
    "https://localhost:5173",
    "http://vstrechya.space:5173",
    "https://vstrechya.space:5173",
    "http://vstrechya.space",
    "https://vstrechya.space",
    "https://engine.vstrechya.space",
    "http://engine.vstrechya.space",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://127.0.0.1:5173",
    "https://localhost:5173",
    "http://vstrechya.space:5173",
    "https://vstrechya.space:5173",
    "http://vstrechya.space",
    "https://vstrechya.space",
    "http://vstrechya.space:8010",
    "https://vstrechya.space:8010",
    "http://engine.vstrechya.space",
    "https://engine.vstrechya.space",
]

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://127.0.0.1:5173",
    "https://localhost:5173",
    "http://vstrechya.space:5173",
    "https://vstrechya.space:5173",
    "http://vstrechya.space",
    "https://vstrechya.space",
    "https://engine.vstrechya.space",
    "http://engine.vstrechya.space",
]

CORS_ALLOW_CREDENTIALS = True

base_structlog_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.filter_by_level,
    # Perform %-style formatting.
    structlog.stdlib.PositionalArgumentsFormatter(),
    # Add a timestamp in ISO 8601 format.
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    # If some value is in bytes, decode it to a unicode str.
    structlog.processors.UnicodeDecoder(),
    # Add callsite parameters.
    structlog.processors.CallsiteParameterAdder(
        {
            structlog.processors.CallsiteParameter.FILENAME,
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.LINENO,
        }
    ),
]

base_structlog_formatter = [structlog.stdlib.ProcessorFormatter.wrap_for_formatter]

structlog.configure(
    processors=base_structlog_processors + base_structlog_formatter,  # type: ignore
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(colors=True),
        },
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored_console",
        },
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json_formatter",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django_structlog": {
            "level": "DEBUG",
        },
        # Django Structlog request middlewares
        "django_structlog.middlewares": {
            "level": "INFO",
        },
        # DB logs
        "django.db.backends": {
            "level": "CRITICAL",
        },
        # Use structlog middleware
        "django.server": {
            "handlers": ["null"],
            "propagate": False,
        },
        # Use structlog middleware
        "django.request": {
            "handlers": ["null"],
            "propagate": False,
        },
        # Use structlog middleware
        "django.channels.server": {
            "handlers": ["null"],
            "propagate": False,
        },
        # Use structlog middleware
        "werkzeug": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

DJOSER = {
    "USER_CREATE_PASSWORD_RETYPE": True,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "LOGIN_FIELD": "email",
    #'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    #'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    "ACTIVATION_URL": "auth/activate/{uid}/{token}/",
    "SEND_ACTIVATION_EMAIL": False,
    "SERIALIZERS": {
        "user_create": "account.serializers.UserCreateSerializer",
        "user": "account.serializers.UserSerializer",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.mail.ru"
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

AWS_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_URL = "https://digital-portfolio.hb.ru-msk.vkcs.cloud/"
AWS_ENDPOINT_URL = "https://hb.ru-msk.vkcs.cloud/"


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

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "messenger.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_prometheus.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis-qoovee/0",
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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        # 'rest_framework.permissions.IsAdminUser',
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        #'rest_framework.authentication.TokenAuthentication',
        "account.auth.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=3),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
    "UPDATE_LAST_LOGIN": True,
    # "USER_AUTHENTICATION_RULE": "accounts.auth.default_user_authentication_rule",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Vstrechya API",
    "DESCRIPTION": "vstrechya.space API Endpoints",
    "VERSION": "1.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [
                {
                    "address": "redis://redis-qoovee/2",
                }
            ]
        },
    }
}

LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
