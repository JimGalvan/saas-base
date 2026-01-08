"""
QA/Staging settings for Django SaaS Starter
"""
import os
import dj_database_url
from .base import *

# Enable DEBUG for QA to get more detailed error information
DEBUG = True

# Set environment flag
ENVIRONMENT = "qa"

# QA-specific CSRF trusted origins - update with your QA domain
CSRF_TRUSTED_ORIGINS = [
    "https://your-qa-app.herokuapp.com",  # Update this
    "https://your-qa-app.up.railway.app",  # Update this
]

# Security
SECRET_KEY = os.getenv("SECRET_KEY")

# AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "us-east-1")

ALLOWED_HOSTS = ["*"]

# Database - use PostgreSQL in QA
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600
    )
}

# Static files settings
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Stripe Settings - use test API keys for QA environment
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
STRIPE_ACCOUNT_WEBHOOK_SECRET = os.getenv('STRIPE_ACCOUNT_WEBHOOK_SECRET', '')
STRIPE_CONNECT_WEBHOOK_SECRET = os.getenv('STRIPE_CONNECT_WEBHOOK_SECRET', '')

# reCAPTCHA Settings
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')
DISABLE_RECAPTCHA = False

# SSL settings - enable for QA environment
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# WhiteNoise settings
WHITENOISE_MANIFEST_STRICT = False  # Allow missing manifest entries in QA

# Override the STORAGES setting from base.py to use S3
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
}

# Email settings for QA (using SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.getenv('EMAIL_PORT', '587')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or 'noreply@example.com'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
