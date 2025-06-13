import ipaddress
import json
import os

from configparser import ConfigParser
from pathlib import Path

# Project directory (where settings.py is)
PROJECT_DIR = Path(__file__).resolve().parent

# Repository root directory
BASE_DIR = PROJECT_DIR.parent.parent

# Shared var directory (for logs, cache, etc.)
VAR_DIR = BASE_DIR / "var"

# Read configuration from ini file

config = ConfigParser(converters={"literal": json.loads}, interpolation=None)
config.read(
    [
        os.environ.get("APP_SETTINGS", PROJECT_DIR / "local.ini"),
        PROJECT_DIR / "local.ini",
    ]
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.getliteral("app", "secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean("app", "debug", fallback=False)

if DEBUG:
    # Also watch local.ini for changes in debug mode
    from django.utils import autoreload

    def watch_local_ini(signal, sender):
        sender.extra_files.add(PROJECT_DIR / "local.ini")

    autoreload.autoreload_started.connect(watch_local_ini)

ALLOWED_HOSTS = config.getliteral("app", "allowed_hosts")

# Trust X-Forwarded-Host header in development
USE_X_FORWARDED_HOST = DEBUG

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True  # Adds 'X-Content-Type-Options: nosniff' header
SECURE_BROWSER_XSS_FILTER = True  # Adds 'X-XSS-Protection: 1; mode=block' header
X_FRAME_OPTIONS = "DENY"  # Don't allow this site to be framed
SECURE_REFERRER_POLICY = (
    "strict-origin, strict-origin-when-cross-origin"  # Adds 'Referrer-Policy' header
)
SILENCED_SYSTEM_CHECKS = [
    # These are all handled by nginx, so Django doesn't need to worry about them
    "security.W004",  # You have not set a value for the SECURE_HSTS_SECONDS setting
    "security.W008",  # SECURE_SSL_REDIRECT setting is not set to True
    *config.getliteral("app", "silenced_system_checks", fallback=[]),
]

# Application definition

INSTALLED_APPS = [
    "bandit",
    "leukeleu_django_checks",
    "leukeleu_django_gdpr",
    # Django
    "hidp_django_admin",  # Should be above "django.contrib.admin" for templates to work
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Hello, ID Please
    "hidp",
    "hidp.accounts",
    "hidp.csp",
    "hidp.federated",
    "hidp.otp",
    "django_otp",
    "django_otp.plugins.otp_static",
    "django_otp.plugins.otp_totp",
    # HIdP Django Admin Sandbox
    "hidp_django_admin_sandbox.accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Hello, ID Please
    "hidp.rate_limit.middleware.RateLimitMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "hidp.otp.middleware.OTPRequiredMiddleware",
]

ROOT_URLCONF = "hidp_django_admin_sandbox.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(PROJECT_DIR / "../templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hidp_django_admin_sandbox.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config.getliteral("app", "db_host", fallback=""),
        "NAME": config.getliteral("app", "db_name"),
        "USER": config.getliteral("app", "db_user"),
        "OPTIONS": {
            "passfile": Path("~/.pgpass").expanduser(),
        },
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# When upgrading existing projects use django.db.models.AutoField
# to avoid changing the primary key of existing models
# DEFAULT_AUTO_FIELD = "django.db.models.AutoField"  # noqa: ERA001

# When creating new projects django.db.models.BigAutoField is preferred
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "nl-nl"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [PROJECT_DIR / "locale"]

# Media files (user uploads)

MEDIA_URL = "/media/"

if DEBUG:
    # MEDIA_ROOT defaults to VAR_DIR/public/media/ in debug mode
    MEDIA_ROOT = Path(
        config.getliteral("app", "media_root", fallback=VAR_DIR / "public/media")
    )
else:
    # Require MEDIA_ROOT to be configured
    MEDIA_ROOT = Path(config.getliteral("app", "media_root"))

# File upload permissions
# https://docs.djangoproject.com/en/4.2/ref/settings/#file-upload-permissions
FILE_UPLOAD_PERMISSIONS = 0o644

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

if DEBUG:
    # STATIC_ROOT defaults to VAR_DIR/public/static/ in debug mode
    STATIC_ROOT = Path(
        config.getliteral("app", "static_root", fallback=VAR_DIR / "public/static")
    )
else:
    # Require STATIC_ROOT to be configured
    STATIC_ROOT = Path(config.getliteral("app", "static_root"))

# File storage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "hidp_django_admin_sandbox.storage.staticfiles.SelectiveManifestStaticFilesStorage",  # noqa: E501, RUF100
    },
}

# Email backends
EMAIL_BANDIT = config.getliteral("app", "email_bandit", fallback=False)

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_HOST = config.getliteral("app", "email_host", fallback="localhost")
    EMAIL_PORT = config.getliteral("app", "email_port", fallback=25)
    EMAIL_HOST_USER = config.getliteral("app", "email_host_user", fallback="")
    EMAIL_HOST_PASSWORD = config.getliteral("app", "email_host_password", fallback="")
    EMAIL_USE_TLS = config.getliteral("app", "email_use_tls", fallback=False)
    EMAIL_USE_SSL = config.getliteral("app", "email_use_ssl", fallback=False)

    if EMAIL_BANDIT:
        EMAIL_BACKEND = "bandit.backends.smtp.HijackSMTPBackend"
        BANDIT_EMAIL = config.getliteral("app", "bandit_email")
        BANDIT_WHITELIST = config.getliteral(
            "app", "bandit_whitelist", fallback=["leukeleu.nl"]
        )

DEFAULT_FROM_EMAIL = config.getliteral("app", "default_from_email")

# Django GDPR
DJANGO_GDPR_YML_DIR = PROJECT_DIR.parent


class InternalIPList:
    """
    A fake list that checks if a given ip address
    is local (loopback) or internal (private)
    """

    def __contains__(self, item):
        address = ipaddress.ip_address(item)
        return address.is_loopback or address.is_private


if DEBUG:
    INTERNAL_IPS = InternalIPList()

# Hello, ID Please

LOGIN_URL = "hidp_accounts:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

OTP_TOTP_ISSUER = "HIdP Django Admin Sandbox"

REGISTRATION_ENABLED = False
