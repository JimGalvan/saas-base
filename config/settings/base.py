"""
Django settings for Django SaaS Starter project.

Based on NexMenus infrastructure - a production-ready Django SaaS boilerplate.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

# Maintenance mode setting is now controlled via the admin panel
# The actual value is retrieved dynamically in the middleware
# We keep this as a fallback
MAINTENANCE_MODE = os.environ.get('MAINTENANCE_MODE', 'False') == 'True'

# Determine BASE_URL based on environment
if os.environ.get("ENV") == "production":
    BASE_URL = os.environ.get("BASE_URL", "https://yourdomain.com")
else:
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
# This should be set in environment-specific settings
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
# This should be overridden in production settings via environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Required for django-allauth
    "django.contrib.humanize",  # For template tags like naturalday

    # Third-party apps
    "django_browser_reload",  # Auto-reload during development
    "django_htmx",  # HTMX integration
    "allauth",  # Authentication
    "allauth.account",  # Account management
    "django_recaptcha",  # reCAPTCHA integration
    "django_ratelimit",  # Rate limiting

    # Local apps (customize these for your project)
    # Note: These will be created in subsequent phases
    "apps.core",  # Core utilities and base models
    "apps.accounts",  # User management
    "apps.subscription",  # Stripe subscription management
    "apps.maintenance",  # Maintenance mode
    "apps.webhooks",  # Webhook handling
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static file serving
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Internationalization
    "apps.core.middleware.TranslationDebugMiddleware",  # Translation debug
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "apps.core.middleware.MaintenanceModeMiddleware",  # Maintenance mode
    "apps.core.middleware.FirebaseMiddleware",  # Firebase service worker stub
]

ROOT_URLCONF = "config.urls"

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
                # Custom context processors (will add in Phase 2)
                "apps.core.context_processors.environment",
                "apps.core.context_processors.user_subscription",
                "apps.core.context_processors.recaptcha",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# This will be overridden in environment-specific settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
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

LANGUAGES = [
    ('en', _('English')),
    ('es', _('Spanish')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication backends
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of allauth
    "django.contrib.auth.backends.ModelBackend",
    # allauth specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Custom User Model
AUTH_USER_MODEL = "accounts.User"

# Django Allauth Settings
ACCOUNT_FORMS = {
    "signup": "apps.accounts.forms.CaptchaSignupForm",
    "login": "apps.accounts.forms.CustomLoginForm",
}
SITE_ID = 1
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/accounts/login/"
# django-allauth modern settings (allauth >= 65.0)
ACCOUNT_LOGIN_METHODS = {'email'}  # Login via email only
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # Required fields for signup
ACCOUNT_EMAIL_VERIFICATION = "none"  # Change to "mandatory" in production
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = False

# Comprehensive rate limiting for authentication endpoints
ACCOUNT_RATE_LIMITS = {
    # Login attempts - limit to 30 per minute per IP
    "login": "30/m/ip",
    # Failed login attempts - 10 per IP per minute, and 5 per username/email in 5 minutes
    "login_failed": "10/m/ip,5/5m/key",
    # Signup - limit to 2 per minute per IP
    "signup": "2/m/ip",
    # Password reset request - 20 per minute per IP, 5 per minute per email
    "reset_password": "20/m/ip,5/m/key",
    # Password reset from key (clicking link in email) - 20 per minute per IP
    "reset_password_from_key": "20/m/ip",
    # Change password (for authenticated users) - 5 per minute per user
    "change_password": "5/m/user",
    # Email management - 10 per minute per user
    "manage_email": "10/m/user",
    # Email confirmation - 1 per 3 minutes for links
    "confirm_email": "1/3m/key",
}

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # Use console for development
EMAIL_HOST = str(os.getenv("EMAIL_HOST", ""))
EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER", ""))
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or "noreply@example.com"
EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD", ""))
EMAIL_PORT = str(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
EMAIL_FAIL_SILENTLY = True
ACCOUNT_UNIQUE_EMAIL = True

# Allauth adapter
ACCOUNT_ADAPTER = "apps.accounts.adapters.AccountAdapter"

# Security settings
SESSION_COOKIE_SECURE = (
    os.environ.get("ENV") == "production"
)  # Only use secure cookies in production
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"  # Prevents your site from being framed

# HTTPS settings (for production)
if os.environ.get("ENV") == "production":
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Storage configuration
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        # For development, use filesystem. For production, use S3 (configure in prod.py)
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# Redis configuration
REDIS_URL_FROM_ENV = os.getenv('REDIS_URL')
REDIS_HOST = os.getenv('REDISHOST') or '127.0.0.1'
REDIS_PORT = os.getenv('REDISPORT') or '6379'
REDIS_DB = os.getenv('REDIS_DB') or '1'

# Determine effective Redis location
_redis_location = None
IS_PRODUCTION_ENV = os.environ.get("ENV") == "production"

if REDIS_URL_FROM_ENV and REDIS_URL_FROM_ENV.strip():
    _redis_location = REDIS_URL_FROM_ENV.strip()
elif IS_PRODUCTION_ENV:
    # In production, REDIS_URL must be set
    raise ImproperlyConfigured(
        "In production (ENV=production), REDIS_URL environment variable must be set to a valid, "
        "non-empty Redis connection string (e.g., redis://:password@host:port/db)."
    )
else:
    # For development, construct fallback URL
    _redis_location = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# Cache settings for django-ratelimit and general caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": _redis_location,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "ratelimit": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": _redis_location,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Ratelimit specific settings
RATELIMIT_USE_CACHE = 'default'

# Celery Configuration Options
# Using Redis as the broker and result backend

if REDIS_URL_FROM_ENV:
    CELERY_BROKER_URL = REDIS_URL_FROM_ENV
    CELERY_RESULT_BACKEND = REDIS_URL_FROM_ENV
else:
    # Fallback for local development
    REDIS_HOST = os.getenv('REDISHOST', '127.0.0.1')
    REDIS_PORT = os.getenv('REDISPORT', '6379')
    REDIS_DB_CELERY = os.getenv('REDIS_DB_CELERY', '0')
    CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_CELERY}"
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_CELERY}"

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# reCAPTCHA settings (get keys from https://www.google.com/recaptcha/admin)
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')
DISABLE_RECAPTCHA = os.environ.get('DISABLE_RECAPTCHA', 'False') == 'True'

# Stripe settings (for subscription management)
STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_ACCOUNT_WEBHOOK_SECRET = os.environ.get('STRIPE_ACCOUNT_WEBHOOK_SECRET', '')
STRIPE_CONNECT_WEBHOOK_SECRET = os.environ.get('STRIPE_CONNECT_WEBHOOK_SECRET', '')

# AWS S3 settings (for media file storage in production)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com' if AWS_STORAGE_BUCKET_NAME else None
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
