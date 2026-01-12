# Django SaaS Starter - Extraction Plan from NexMenus

**Project:** Extract reusable SaaS infrastructure from NexMenus into a generic Django SaaS boilerplate
**Date Created:** 2026-01-02
**Date Started:** 2026-01-07
**Status:** ✅ Phase 1 Complete - In Progress
**Estimated Effort:** 4-6 days
**Target Name:** `django-saas-starter` (configurable)
**Project Location:** C:/Users/jimmy/PycharmProjects/django-saas-starter/

---

## 🎯 Progress Tracker

### Overall Progress: 27% (3/11 phases complete)

| Phase | Status | Date Completed | Notes |
|-------|--------|----------------|-------|
| Phase 1: Project Initialization | ✅ **COMPLETE** | 2026-01-07 | Django project created, settings configured, Git initialized |
| Phase 2: Core Infrastructure | ✅ **COMPLETE** | 2026-01-08 | BaseModel, S3 utils, middleware, context processors extracted |
| Phase 3: User & Authentication | ✅ **COMPLETE** | 2026-01-11 | User model, forms, adapter, admin configured |
| Phase 4: Subscription System | 📋 Planned | - | Stripe integration ready |
| Phase 5: Maintenance Mode | 📋 Planned | - | Maintenance app ready |
| Phase 6: Webhooks | 📋 Planned | - | Webhook infrastructure planned |
| Phase 7: Templates & Static | 📋 Planned | - | Template extraction planned |
| Phase 8: Configuration & URLs | 📋 Planned | - | URL configuration planned |
| Phase 9: Documentation | 📋 Planned | - | Comprehensive docs needed |
| Phase 10: Testing & Validation | 📋 Planned | - | Full testing suite |
| Phase 11: Polish & Release | 📋 Planned | - | Final cleanup and release |

### Latest Update: 2026-01-11
**Phase 3 Complete** - User & Authentication system extracted and configured:
- ✅ Custom User model with UUID primary key
- ✅ Subscription status checking methods (has_active_subscription, has_ever_had_subscription)
- ✅ Authentication forms with reCAPTCHA integration
- ✅ Custom allauth adapter for authentication customization
- ✅ User admin interface with UUID display
- ✅ Settings updated for AUTH_USER_MODEL and ACCOUNT_FORMS
- ✅ Migrations generated and applied successfully
- ✅ Commit: 0c5ba59

**Next Steps:** Phase 4: Subscription System - Extract Stripe subscription infrastructure

---

## Table of Contents
- [Executive Summary](#executive-summary)
- [Analysis Overview](#analysis-overview)
- [Reusable Components Inventory](#reusable-components-inventory)
- [Extraction Strategy](#extraction-strategy)
- [Detailed Implementation Plan](#detailed-implementation-plan)
- [File Migration Checklist](#file-migration-checklist)
- [Testing & Validation](#testing--validation)
- [Documentation Requirements](#documentation-requirements)

---

## Executive Summary

### Viability Assessment: ✅ HIGHLY VIABLE

NexMenus contains **60-70% reusable infrastructure code** suitable for a production-ready SaaS boilerplate. The codebase demonstrates:
- Excellent separation of concerns
- Modern Django 5.1+ patterns
- Production-tested infrastructure
- Comprehensive security implementations
- Scalable architecture (Celery, Redis, S3)

### Key Statistics
- **Reusable Apps:** 4 complete (accounts, subscription, maintenance, core utils)
- **Reusable Modules:** 8+ (settings, middleware, webhooks, storage, etc.)
- **Domain-Specific Apps to Exclude:** 5 (menu, ordering, catalog, blog, test_tools)
- **Lines of Reusable Code:** ~3,000-4,000 (estimated)

---

## Analysis Overview

### Architecture Strengths

#### ✅ Production-Ready Infrastructure
- Multi-environment settings (dev/qa/prod)
- Heroku deployment configuration
- Gunicorn + Celery worker processes
- Redis caching and rate limiting
- S3 media storage
- Sentry integration ready

#### ✅ Security First
- Comprehensive rate limiting on auth endpoints
- HSTS, XSS, CSRF protection
- Environment-aware security settings
- Session security hardening
- reCAPTCHA integration

#### ✅ Scalable Design
- Async task processing (Celery)
- Redis for caching and message broker
- S3 for distributed media storage
- UUID primary keys for distributed systems
- Connection pooling ready

#### ✅ Developer Experience
- Clear app separation
- Abstract base models
- Reusable middleware
- Comprehensive error handling
- i18n/l10n support built-in

### Current Challenges

#### ⚠️ User Model Location
**Issue:** User model resides in `menu/` app
**Impact:** Creates coupling with domain logic
**Solution:** Extract to `accounts/` app

#### ⚠️ Context Processors
**Issue:** Base settings reference menu-specific context processors
**Location:** `NexMenus/settings/base.py` lines 97-99
**Solution:** Move to generic `core/` app

#### ⚠️ Mixed Utilities
**Issue:** `menu/utils.py` contains both S3 utilities and domain logic
**Solution:** Split into `core/storage.py` (S3) and domain utils

---

## Reusable Components Inventory

### 1. Authentication & User Management ⭐⭐⭐
**Priority:** CRITICAL
**Reusability Score:** 85%

**Files to Extract:**
```
accounts/
├── forms.py                    # CaptchaSignupForm, CustomLoginForm
├── adapters.py                 # Custom allauth adapter (if exists)
└── migrations/                 # Will need regeneration

menu/models.py                  # Extract User model only
  → Move to accounts/models.py
```

**Features:**
- Custom User with UUID primary key
- django-allauth email-based authentication
- reCAPTCHA on signup
- Comprehensive rate limiting
- Custom error messages

**Modifications Needed:**
- Remove `stripe_connect_completed` (domain-specific)
- Remove `has_completed_onboarding` (domain-specific)
- Remove `onboarding_step` (domain-specific)
- Keep or generalize `has_active_plus()` → `has_active_subscription()`

---

### 2. Subscription Management ⭐⭐⭐
**Priority:** CRITICAL
**Reusability Score:** 90%

**Files to Extract:**
```
subscription/
├── models.py                   # Customer, Subscription
├── utils.py                    # Stripe helper functions
├── enums.py                    # SubscriptionStatus, PlanType
├── views.py                    # Subscription views
├── urls.py                     # Subscription URL patterns
├── forms.py                    # Subscription forms (if exists)
├── templates/subscription/     # Subscription templates
└── migrations/                 # Will need regeneration
```

**Features:**
- Complete Stripe integration
- Customer and Subscription models
- Webhook handling
- Plan tier management (FREE/PLUS)
- Subscription status sync utilities

**Modifications Needed:**
- Make plan types configurable (FREE/PLUS → environment-driven)
- Ensure generic enough for any SaaS

---

### 3. Settings Architecture ⭐⭐⭐
**Priority:** CRITICAL
**Reusability Score:** 100%

**Files to Extract:**
```
NexMenus/settings/
├── __init__.py                 # Auto-load based on ENV
├── base.py                     # Core settings
├── development.py              # Dev overrides
├── qa.py                       # QA/staging overrides
└── prod.py                     # Production settings
```

**Features:**
- Environment-based configuration (ENV variable)
- Redis URL construction with fallbacks
- Celery configuration
- Security settings per environment
- STORAGES configuration (S3 + WhiteNoise)

**Modifications Needed:**
- Update `AUTH_USER_MODEL` path
- Remove domain-specific context processors
- Update `INSTALLED_APPS` list
- Generic `BASE_URL` configuration

---

### 4. Maintenance Mode System ⭐⭐⭐
**Priority:** HIGH
**Reusability Score:** 100%

**Files to Extract:**
```
maintenance/
├── models.py                   # MaintenanceMode singleton
├── admin.py                    # Admin interface
├── views.py                    # Maintenance views (if exists)
├── management/
│   └── commands/
│       └── maintenance_mode.py # CLI toggle command
├── migrations/                 # Will need regeneration
└── templates/maintenance/      # Maintenance page templates
```

**Features:**
- Database-backed toggle
- Admin interface
- Middleware with path exemptions
- Caching for performance
- Custom maintenance messages

**Modifications Needed:**
- None - 100% reusable

---

### 5. Core Infrastructure ⭐⭐⭐
**Priority:** CRITICAL
**Reusability Score:** 95%

**Files to Create/Extract:**
```
core/                           # NEW APP
├── models.py                   # BaseModel abstract class
├── storage.py                  # S3 utilities
├── utils.py                    # Generic utilities
├── middleware.py               # Reusable middleware
└── context_processors.py       # Generic context processors
```

**Extract From:**
- `menu/models.py` → `BaseModel` class only
- `menu/utils.py` → S3 functions (get_s3_client, delete_s3_objects)
- `NexMenus/common_utils.py` → All utilities
- `NexMenus/middleware.py` → All middleware

**Features:**
- BaseModel with UUID, timestamps, ordering
- S3 client management with caching
- S3 object deletion utilities
- Environment variable helpers
- Maintenance middleware
- Translation debug middleware
- Firebase stub middleware

**Modifications Needed:**
- Consolidate into single `core/` app
- Remove domain-specific functions from utils

---

### 6. Webhook Infrastructure ⭐⭐
**Priority:** HIGH
**Reusability Score:** 75%

**Files to Extract:**
```
webhooks/
├── handlers.py                 # Webhook routers
├── models.py                   # WebhookEvent model (if in ordering/)
└── tasks.py                    # Async webhook processing (if exists)
```

**Features:**
- Stripe webhook validation
- Signature verification
- Event routing (account vs connect)
- Async processing pattern
- Event storage for debugging

**Modifications Needed:**
- Abstract webhook handlers into base classes
- Make event routing configurable
- Separate Stripe-specific from generic webhook patterns

---

### 7. Template Structure ⭐⭐
**Priority:** MEDIUM
**Reusability Score:** 80%

**Files to Extract:**
```
templates/
├── base.html                   # Main base template
├── layout/
│   ├── topbar.html             # Navigation bar
│   ├── footer.html             # Footer component
│   └── sidebar.html            # Sidebar component
├── account/                    # Allauth templates (customized)
├── maintenance/
│   ├── maintenance.html        # Maintenance page
│   └── maintenance_htmx.html   # HTMX maintenance partial
├── subscription/               # Subscription templates
├── 403.html                    # Forbidden error
├── 404.html                    # Not found error
├── 429.html                    # Rate limit error
├── 500.html                    # Server error
├── home.html                   # Generic home (modify)
└── landing.html                # Landing page (modify)
```

**Features:**
- Responsive base template
- Mobile-optimized viewport
- Favicon integration
- Google Analytics with dev exclusions
- Component-based layout
- Error pages

**Modifications Needed:**
- Remove "NexMenus" branding
- Generic navigation links
- Placeholder home/landing content
- Update meta tags for generic SaaS

---

### 8. Static Assets ⭐
**Priority:** LOW
**Reusability Score:** 60%

**Files to Extract:**
```
static/
├── css/
│   └── (generic styles only)
├── js/
│   └── (generic utilities only)
├── favicon/                    # Favicon files
│   ├── apple-touch-icon.png
│   ├── favicon-32x32.png
│   ├── favicon-16x16.png
│   └── site.webmanifest
└── sounds/                     # (exclude or make optional)
```

**Modifications Needed:**
- Remove domain-specific CSS
- Keep only utility JavaScript
- Provide placeholder favicon (or generation guide)
- Remove app-specific assets

---

### 9. Internationalization ⭐⭐
**Priority:** MEDIUM
**Reusability Score:** 100%

**Files to Extract:**
```
locale/
├── es/
│   └── LC_MESSAGES/
│       └── (example translations)
└── (structure for other languages)

compile_translations.py         # Translation compilation script
```

**Features:**
- Multi-language support (en/es example)
- i18n URL patterns
- Translation middleware
- JavaScript catalog integration

**Modifications Needed:**
- Keep as example/documentation
- Clear domain-specific translations
- Provide setup guide

---

### 10. Celery & Async Tasks ⭐⭐⭐
**Priority:** HIGH
**Reusability Score:** 100%

**Configuration in Settings:**
- `CELERY_BROKER_URL` with Redis
- `CELERY_RESULT_BACKEND` with Redis
- Task serialization (JSON)
- Beat scheduler setup

**Files to Extract:**
```
NexMenus/celery.py              # Celery app configuration (if exists)
```

**Modifications Needed:**
- None - configuration is generic

---

### 11. Database & Models ⭐⭐
**Priority:** CRITICAL
**Reusability Score:** 100%

**Configuration:**
- PostgreSQL via dj-database-url
- UUID primary keys (in BaseModel)
- Timestamp tracking (in BaseModel)

**Modifications Needed:**
- None - pattern is generic

---

## Extraction Strategy

### Approach: Clean Room Extraction

Rather than forking/renaming, we'll create a fresh Django project and systematically extract components. This ensures:
- Clean git history
- No accidental domain logic leakage
- Opportunity to refactor during extraction
- Clear documentation of what's included

### Project Structure

```
django-saas-starter/
├── README.md
├── LICENSE
├── requirements.txt
├── .env.example
├── .gitignore
├── manage.py
├── pytest.ini
├── conftest.py
│
├── config/                         # Main project package (renamed from NexMenus)
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── qa.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
│
├── apps/                           # All Django apps
│   ├── __init__.py
│   │
│   ├── accounts/                   # User management & auth
│   │   ├── __init__.py
│   │   ├── models.py               # Custom User model
│   │   ├── forms.py                # Auth forms with reCAPTCHA
│   │   ├── adapters.py             # Allauth adapters
│   │   ├── admin.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations/
│   │
│   ├── core/                       # Core infrastructure
│   │   ├── __init__.py
│   │   ├── models.py               # BaseModel abstract class
│   │   ├── storage.py              # S3 utilities
│   │   ├── utils.py                # Helper functions
│   │   ├── middleware.py           # Reusable middleware
│   │   ├── context_processors.py  # Context processors
│   │   └── management/
│   │       └── commands/
│   │
│   ├── subscription/               # Stripe subscriptions
│   │   ├── __init__.py
│   │   ├── models.py               # Customer, Subscription
│   │   ├── enums.py                # Status, Plan enums
│   │   ├── utils.py                # Stripe helpers
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── migrations/
│   │
│   ├── maintenance/                # Maintenance mode
│   │   ├── __init__.py
│   │   ├── models.py               # MaintenanceMode singleton
│   │   ├── admin.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── maintenance_mode.py
│   │   └── migrations/
│   │
│   └── webhooks/                   # Webhook handling
│       ├── __init__.py
│       ├── handlers.py             # Webhook routers
│       ├── models.py               # WebhookEvent
│       └── tasks.py                # Async processing
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── layout/
│   │   ├── topbar.html
│   │   ├── footer.html
│   │   └── sidebar.html
│   ├── account/                    # Allauth templates
│   ├── subscription/
│   ├── maintenance/
│   └── errors/
│       ├── 403.html
│       ├── 404.html
│       ├── 429.html
│       └── 500.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── favicon/
│
├── locale/                         # i18n translations
│   └── es/
│
├── media/                          # Local dev media (gitignored)
├── staticfiles/                    # Collected static (gitignored)
│
└── docs/
    ├── INSTALLATION.md
    ├── DEPLOYMENT.md
    ├── CONFIGURATION.md
    ├── STRIPE_SETUP.md
    └── CUSTOMIZATION.md
```

---

## Detailed Implementation Plan

### Phase 1: Project Initialization (Day 1)
**Goal:** Set up clean project structure with core configuration

#### Task 1.1: Create New Django Project
```bash
# Create new project directory
mkdir django-saas-starter
cd django-saas-starter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install Django
pip install Django==5.1.1

# Create project (use 'config' as project name)
django-admin startproject config .

# Rename settings.py to settings package
mkdir config/settings
touch config/settings/__init__.py
```

**Acceptance Criteria:**
- [x] Django project created
- [x] Settings package structure ready
- [x] Git repository initialized
- [x] Basic .gitignore configured

---

#### Task 1.2: Configure Settings Architecture
**Source Files:**
- `NexMenus/settings/base.py`
- `NexMenus/settings/development.py`
- `NexMenus/settings/qa.py`
- `NexMenus/settings/prod.py`

**Actions:**
1. Copy `base.py` to `config/settings/base.py`
2. Copy environment-specific settings files
3. Update `__init__.py` to auto-load based on ENV
4. Remove domain-specific INSTALLED_APPS (menu, ordering, catalog, blog)
5. Remove domain-specific context processors
6. Update AUTH_USER_MODEL to 'accounts.User'
7. Create `.env.example` with all required variables

**Modifications:**
```python
# config/settings/base.py

# BEFORE (in NexMenus):
INSTALLED_APPS = [
    # ... standard apps ...
    "menu",
    "catalog",
    "subscription",
    # ... etc ...
]

AUTH_USER_MODEL = "menu.User"

TEMPLATES = [
    {
        # ...
        "OPTIONS": {
            "context_processors": [
                # ...
                "menu.context_processors.environment",
                "menu.context_processors.user_subscription",
                "menu.context_processors.recaptcha",
            ],
        },
    },
]

# AFTER (in django-saas-starter):
INSTALLED_APPS = [
    # Django built-ins
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",

    # Third-party
    "django_browser_reload",
    "django_htmx",
    "allauth",
    "allauth.account",
    "django_recaptcha",
    "qr_code",
    "django_ratelimit",

    # Local apps
    "apps.core",
    "apps.accounts",
    "apps.subscription",
    "apps.maintenance",
    "apps.webhooks",
]

AUTH_USER_MODEL = "accounts.User"

TEMPLATES = [
    {
        # ...
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.environment",
                "apps.core.context_processors.user_subscription",
                "apps.core.context_processors.recaptcha",
            ],
        },
    },
]
```

**Acceptance Criteria:**
- [x] Settings architecture copied
- [x] Environment-based loading works
- [x] Domain-specific references removed
- [x] All paths updated to new structure
- [x] .env.example created

---

#### Task 1.3: Create Requirements File
**Source:** `requirements.txt`

**Actions:**
1. Copy `requirements.txt`
2. Remove domain-specific packages (if any)
3. Add comments for optional packages
4. Organize by category

**Output:** `requirements.txt`
```txt
# Core Django
Django==5.1.1
psycopg2-binary==2.9.9
dj-database-url==2.2.0
python-dotenv==1.0.1
gunicorn==23.0.0

# Authentication
django-allauth==65.0.2
django-recaptcha==4.0.0

# Subscriptions
stripe==11.2.0

# Storage & Media
boto3==1.35.41
django-storages==1.14.4
Pillow==10.4.0

# Async Tasks
celery==5.5.2
redis==5.2.1
django-redis==5.4.0

# Utilities
django-htmx==1.19.0
django-ratelimit==4.1.0
django-qr-code==3.1.1
whitenoise==6.9.0
sentry-sdk==2.22.0

# Development
django-debug-toolbar==5.0.1
django-browser-reload==1.15.0
django-extensions==3.2.3

# Testing
pytest==8.3.5
pytest-playwright==0.7.0
playwright==1.51.0
```

**Acceptance Criteria:**
- [x] Requirements file created
- [x] Packages categorized
- [x] Domain-specific packages removed
- [x] Comments added for optional packages

---

#### Task 1.4: Initialize Git & Documentation
**Actions:**
1. Create `.gitignore`
2. Initialize git repository
3. Create initial README.md
4. Create LICENSE file
5. Initial commit

**Files to Create:**
- `.gitignore`
- `README.md`
- `LICENSE`

**Acceptance Criteria:**
- [x] Git repository initialized
- [x] .gitignore configured
- [x] README.md created with basic info
- [x] Initial commit made

---

### Phase 2: Core Infrastructure (Day 1-2)
**Goal:** Extract and configure core utilities and base models

#### Task 2.1: Create Core App
```bash
python manage.py startapp core apps/core
```

**Files to Create:**
1. `apps/core/models.py` - BaseModel
2. `apps/core/storage.py` - S3 utilities
3. `apps/core/utils.py` - Helper functions
4. `apps/core/middleware.py` - Middleware classes
5. `apps/core/context_processors.py` - Context processors

---

#### Task 2.2: Extract BaseModel
**Source:** `menu/models.py` lines 85-92

**Target:** `apps/core/models.py`

**Code:**
```python
# apps/core/models.py
import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model for all models in the application.
    Provides UUID primary key and timestamp tracking.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this record"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this record was last updated"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.__class__.__name__} {self.id}"
```

**Acceptance Criteria:**
- [x] BaseModel extracted
- [x] Documentation added
- [x] Abstract = True
- [x] Default ordering configured

---

#### Task 2.3: Extract S3 Utilities
**Source:** `menu/utils.py` lines 1-94

**Target:** `apps/core/storage.py`

**Code:**
```python
# apps/core/storage.py
import boto3
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

_cached_s3_client = None


def get_s3_client():
    """
    Get or create a cached S3 client.
    Uses singleton pattern to avoid creating multiple clients.

    Returns:
        boto3.client: S3 client instance
    """
    global _cached_s3_client
    if _cached_s3_client is None:
        _cached_s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
    return _cached_s3_client


def delete_s3_objects(prefix=None):
    """
    Delete S3 objects with the given prefix.

    Args:
        prefix (str): The S3 key prefix to match (e.g., 'users/123/uploads/')

    Returns:
        bool: True if objects were deleted successfully, False otherwise

    Example:
        >>> delete_s3_objects('users/abc-123/uploads/')
        True
    """
    if not prefix:
        logger.warning("No prefix provided for S3 object deletion")
        return False  # Require a prefix to avoid accidental deletion

    try:
        s3_client = get_s3_client()
        deleted_count = 0

        # List objects with the given prefix
        logger.info(f"Listing S3 objects with prefix: {prefix}")
        objects = s3_client.list_objects_v2(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Prefix=prefix
        )

        # If there are no objects, return early
        if 'Contents' not in objects:
            logger.info(f"No objects found with prefix: {prefix}")
            return True

        # Delete objects in batches
        while True:
            if 'Contents' in objects:
                delete_keys = {
                    'Objects': [{'Key': obj['Key']} for obj in objects['Contents']]
                }

                if delete_keys['Objects']:
                    deleted_count += len(delete_keys['Objects'])
                    logger.info(f"Deleting {len(delete_keys['Objects'])} objects from S3")
                    s3_client.delete_objects(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                        Delete=delete_keys
                    )

            # Check if there are more objects to process
            if not objects.get('IsTruncated', False):
                break

            # Get next batch
            objects = s3_client.list_objects_v2(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Prefix=prefix,
                ContinuationToken=objects['NextContinuationToken']
            )

        logger.info(f"Successfully deleted {deleted_count} objects with prefix: {prefix}")
        return True

    except Exception as e:
        logger.error(f"Error deleting S3 objects with prefix '{prefix}': {str(e)}")
        return False
```

**Acceptance Criteria:**
- [x] S3 utilities extracted
- [x] Documentation improved
- [x] Error handling preserved
- [x] Logging maintained

---

#### Task 2.4: Extract Common Utilities
**Source:** `NexMenus/common_utils.py`

**Target:** `apps/core/utils.py`

**Code:**
```python
# apps/core/utils.py
import os
from typing import Union, Optional


def get_env_int(key: str, default: Optional[int] = None) -> Optional[int]:
    """
    Get an integer value from environment variables.

    Args:
        key: The environment variable key
        default: Default value if key doesn't exist or value can't be converted

    Returns:
        Integer value or default if not found/invalid

    Example:
        >>> get_env_int('MAX_UPLOAD_SIZE', 5242880)
        5242880
    """
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


def get_env_float(key: str, default: Optional[float] = None) -> Optional[float]:
    """
    Get a float value from environment variables.

    Args:
        key: The environment variable key
        default: Default value if key doesn't exist or value can't be converted

    Returns:
        Float value or default if not found/invalid

    Example:
        >>> get_env_float('TAX_RATE', 0.08)
        0.08
    """
    try:
        return float(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


def get_env_number(
    key: str,
    default: Optional[Union[int, float]] = None
) -> Optional[Union[int, float]]:
    """
    Get a numeric value (int or float) from environment variables.
    Attempts to convert to int first, then float if that fails.

    Args:
        key: The environment variable key
        default: Default value if key doesn't exist or value can't be converted

    Returns:
        Numeric value (int or float) or default if not found/invalid

    Example:
        >>> get_env_number('THRESHOLD', 100)
        100
    """
    value = os.getenv(key)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return default


def get_env_bool(key: str, default: bool = False) -> bool:
    """
    Get a boolean value from environment variables.
    Recognizes: true, yes, 1, on (case-insensitive) as True

    Args:
        key: The environment variable key
        default: Default value if key doesn't exist

    Returns:
        Boolean value

    Example:
        >>> get_env_bool('DEBUG', False)
        False
    """
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ('true', 'yes', '1', 'on')
```

**Acceptance Criteria:**
- [x] All utilities extracted
- [x] Type hints preserved
- [x] Documentation enhanced
- [x] Added `get_env_bool()` helper

---

#### Task 2.5: Extract Middleware
**Source:** `NexMenus/middleware.py`

**Target:** `apps/core/middleware.py`

**Code:**
```python
# apps/core/middleware.py
import re
import logging
from django.shortcuts import render
from django.conf import settings
from django.utils.translation import activate
from django.utils.deprecation import MiddlewareMixin
from apps.maintenance.models import MaintenanceMode

logger = logging.getLogger(__name__)


class MaintenanceModeMiddleware:
    """
    Middleware to check if the site is in maintenance mode.
    Displays maintenance page when active, with exemptions for admin and staff.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Define excluded URL patterns
        self.excluded_urls = [
            r'^/admin/',
            r'^/static/',
            r'^/media/',
            r'^/maintenance/',
            r'^/accounts/login/',
        ]

    def __call__(self, request):
        # Staff/admin users bypass maintenance mode
        if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)

        # Check if maintenance mode is active
        try:
            maintenance_mode = MaintenanceMode.is_maintenance_mode_active()
        except:
            # Fallback to settings if database query fails
            maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)

        if maintenance_mode:
            # Check if current URL should be excluded
            path = request.path_info.lstrip('/')
            full_path = f'/{path}'

            for url_pattern in self.excluded_urls:
                if re.search(url_pattern, full_path):
                    return self.get_response(request)

            # Get customized message
            try:
                message = MaintenanceMode.get_instance().message
            except:
                message = "We're currently making important updates. Please check back soon!"

            # HTMX requests get simplified response
            if request.headers.get('HX-Request'):
                return render(
                    request,
                    'maintenance/maintenance_htmx.html',
                    {'message': message},
                    status=503
                )

            # All other requests get full maintenance page
            return render(
                request,
                'maintenance/maintenance.html',
                {'message': message},
                status=503
            )

        return self.get_response(request)


class TranslationDebugMiddleware(MiddlewareMixin):
    """
    Middleware to ensure translations are loaded correctly.
    Useful for debugging i18n issues.
    """

    def process_request(self, request):
        """Ensure proper language activation."""
        # Get language from session, cookie, or default
        language = (
            request.session.get('_language') or
            request.COOKIES.get('django_language') or
            request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME) or
            settings.LANGUAGE_CODE
        )

        # Activate the language
        if language:
            activate(language)

        # Debug log
        if settings.DEBUG:
            logger.debug(f"Active language: {language}")

        return None

    def process_response(self, request, response):
        """Add language debugging headers in development."""
        if settings.DEBUG:
            language = getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
            response['X-Language'] = language
        return response


class FirebaseMiddleware:
    """
    Middleware that handles requests to Firebase service worker.
    Returns 204 No Content to prevent 404 errors.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/firebase-messaging-sw.js':
            from django.http import HttpResponse
            return HttpResponse(status=204)
        return self.get_response(request)
```

**Acceptance Criteria:**
- [x] All middleware extracted
- [x] Documentation added
- [x] Import paths updated
- [x] Generic enough for any SaaS

---

#### Task 2.6: Create Context Processors
**Source:** Extract from `menu/context_processors.py` (if exists) or create new

**Target:** `apps/core/context_processors.py`

**Code:**
```python
# apps/core/context_processors.py
from django.conf import settings


def environment(request):
    """
    Add environment variables to template context.
    Useful for conditional rendering in templates.
    """
    return {
        'DEBUG': settings.DEBUG,
        'ENV': getattr(settings, 'ENV', 'development'),
        'BASE_URL': getattr(settings, 'BASE_URL', 'http://localhost:8000'),
    }


def recaptcha(request):
    """
    Add reCAPTCHA site key to template context.
    """
    return {
        'RECAPTCHA_SITE_KEY': getattr(settings, 'RECAPTCHA_PUBLIC_KEY', ''),
        'RECAPTCHA_ENABLED': not getattr(settings, 'DISABLE_RECAPTCHA', False),
    }


def user_subscription(request):
    """
    Add user subscription status to template context.
    Only adds data for authenticated users with subscriptions.
    """
    if not request.user.is_authenticated:
        return {}

    try:
        # Try to get subscription from user
        subscription = request.user.customer.subscription_set.first()
        if subscription:
            return {
                'user_subscription': subscription,
                'has_active_subscription': subscription.is_active,
            }
    except:
        pass

    return {
        'user_subscription': None,
        'has_active_subscription': False,
    }
```

**Acceptance Criteria:**
- [x] Context processors created
- [x] Generic and reusable
- [x] Documentation added
- [x] Error handling included

---

### Phase 3: User & Authentication (Day 2)
**Goal:** Extract and configure user authentication system

#### Task 3.1: Create Accounts App
```bash
python manage.py startapp accounts apps/accounts
```

**Files to Create:**
1. `apps/accounts/models.py` - User model
2. `apps/accounts/forms.py` - Auth forms
3. `apps/accounts/adapters.py` - Allauth adapter
4. `apps/accounts/admin.py` - User admin

---

#### Task 3.2: Extract User Model
**Source:** `menu/models.py` lines 25-83

**Target:** `apps/accounts/models.py`

**Code:**
```python
# apps/accounts/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with UUID primary key and subscription integration.

    Extends Django's AbstractUser to use UUID instead of auto-increment ID
    for better distributed system support and security.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this user"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when user account was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when user account was last updated"
    )

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return self.email or self.username

    def has_active_subscription(self):
        """
        Check if the user currently has an active subscription.

        Returns:
            bool: True if user has active subscription, False otherwise
        """
        try:
            from apps.subscription.enums import PlanType
            subscription = self.customer.subscription_set.first()
            return subscription and subscription.plan == PlanType.PLUS
        except:
            return False

    def has_ever_had_subscription(self):
        """
        Check if the user has ever had a subscription.

        Note: Currently checks only current status, but can be expanded
        to check subscription history if that data is available.

        Returns:
            bool: True if user has/had subscription
        """
        return self.has_active_subscription()
```

**Modifications Made:**
- ❌ Removed `has_completed_onboarding` (domain-specific)
- ❌ Removed `has_skipped_onboarding` (domain-specific)
- ❌ Removed `onboarding_step` (domain-specific)
- ❌ Removed `stripe_connect_completed` (domain-specific)
- ❌ Removed `update_stripe_connect_status()` method (domain-specific)
- ✅ Renamed `has_active_plus()` → `has_active_subscription()`
- ✅ Renamed `has_ever_had_plus()` → `has_ever_had_subscription()`

**Acceptance Criteria:**
- [x] User model extracted
- [x] Domain-specific fields removed
- [x] Subscription methods generalized
- [x] Documentation added
- [x] Meta class configured

---

#### Task 3.3: Extract Authentication Forms
**Source:** `accounts/forms.py`

**Target:** `apps/accounts/forms.py`

**Code:** Copy as-is (already generic)

**Acceptance Criteria:**
- [x] Forms copied
- [x] reCAPTCHA integration preserved
- [x] Custom error messages included

---

#### Task 3.4: Create Allauth Adapter
**Source:** Referenced in settings as `menu.adapters.AccountAdapter`

**Target:** `apps/accounts/adapters.py`

**Action:** Check if file exists in NexMenu, if so, copy it. If not, create basic adapter.

---

#### Task 3.5: Configure User Admin
**Target:** `apps/accounts/admin.py`

**Code:**
```python
# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for User model.
    Includes UUID display and subscription status.
    """

    list_display = [
        'email',
        'username',
        'is_active',
        'is_staff',
        'has_active_subscription',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser',
        'created_at',
    ]

    search_fields = [
        'email',
        'username',
        'first_name',
        'last_name',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'last_login',
        'date_joined',
    ]

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
        ('System Info', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )
```

**Acceptance Criteria:**
- [x] Admin configured
- [x] UUID displayed
- [x] Subscription status shown
- [x] Proper fieldsets

---

### Phase 4: Subscription System (Day 2-3)
**Goal:** Extract complete Stripe subscription infrastructure

#### Task 4.1: Create Subscription App
```bash
python manage.py startapp subscription apps/subscription
```

---

#### Task 4.2: Extract Subscription Models
**Source:** `subscription/models.py`, `subscription/enums.py`

**Target:**
- `apps/subscription/models.py`
- `apps/subscription/enums.py`

**Actions:**
1. Copy `enums.py` entirely (generic)
2. Copy `models.py` entirely (generic)
3. Update import for BaseModel: `from apps.core.models import BaseModel`

**Acceptance Criteria:**
- [x] Models extracted
- [x] Enums extracted
- [x] Imports updated
- [x] BaseModel inheritance correct

---

#### Task 4.3: Extract Subscription Utilities
**Source:** `subscription/utils.py`

**Target:** `apps/subscription/utils.py`

**Code:** Copy as-is (already generic Stripe utilities)

**Acceptance Criteria:**
- [x] Utilities copied
- [x] Stripe integration preserved
- [x] All helper functions included

---

#### Task 4.4: Extract Subscription Views & URLs
**Source:**
- `subscription/views.py`
- `subscription/urls.py`

**Target:**
- `apps/subscription/views.py`
- `apps/subscription/urls.py`

**Actions:** Copy files, update template paths if needed

**Acceptance Criteria:**
- [x] Views extracted
- [x] URLs extracted
- [x] Template paths updated

---

#### Task 4.5: Extract Subscription Templates
**Source:** `templates/subscription/`

**Target:** `templates/subscription/`

**Actions:**
1. Copy all subscription templates
2. Remove domain-specific branding
3. Update references to generic terminology

**Acceptance Criteria:**
- [x] Templates copied
- [x] Branding removed
- [x] Generic terminology used

---

### Phase 5: Maintenance Mode (Day 3)
**Goal:** Extract maintenance mode system

#### Task 5.1: Copy Maintenance App
**Source:** `maintenance/`

**Target:** `apps/maintenance/`

**Actions:**
1. Copy entire app directory
2. Update any imports if needed
3. Verify admin integration

**Files to Copy:**
```
maintenance/
├── __init__.py
├── models.py                   # Copy as-is
├── admin.py                    # Copy as-is
├── apps.py                     # Copy as-is
├── management/
│   └── commands/
│       └── maintenance_mode.py # Copy as-is
└── migrations/                 # Will regenerate
```

**Acceptance Criteria:**
- [x] App copied entirely
- [x] Admin registered
- [x] Management command works
- [x] Middleware integrated (already done in Phase 2)

---

#### Task 5.2: Extract Maintenance Templates
**Source:** `templates/maintenance/`

**Target:** `templates/maintenance/`

**Actions:**
1. Copy `maintenance.html`
2. Copy `maintenance_htmx.html`
3. Remove branding

**Acceptance Criteria:**
- [x] Templates copied
- [x] Generic messaging
- [x] Styling preserved

---

### Phase 6: Webhooks (Day 3)
**Goal:** Extract webhook infrastructure

#### Task 6.1: Create Webhooks Package
**Source:** `webhooks/handlers.py`

**Target:** `apps/webhooks/`

**Actions:**
1. Create app directory structure
2. Extract webhook handlers
3. Abstract for generic use
4. Create WebhookEvent model (if in ordering app)

**Files to Create:**
```
apps/webhooks/
├── __init__.py
├── models.py                   # WebhookEvent model
├── handlers.py                 # Webhook routers
├── tasks.py                    # Async processing (if exists)
└── admin.py                    # Webhook admin
```

---

#### Task 6.2: Extract Webhook Event Model
**Source:** `ordering/models.py` (WebhookEvent, if exists)

**Target:** `apps/webhooks/models.py`

**Actions:**
1. Extract WebhookEvent model
2. Update to inherit from BaseModel
3. Make generic (remove domain-specific fields)

---

#### Task 6.3: Abstract Webhook Handlers
**Source:** `webhooks/handlers.py`

**Target:** `apps/webhooks/handlers.py`

**Actions:**
1. Copy webhook validation logic
2. Keep Stripe-specific handlers as examples
3. Add documentation for customization
4. Update import paths

**Modifications:**
```python
# apps/webhooks/handlers.py

# BEFORE (references ordering models):
from ordering.models import WebhookEvent, WebhookEventStatus
from ordering.tasks import process_webhook_event_task

# AFTER (uses local models):
from apps.webhooks.models import WebhookEvent, WebhookEventStatus
from apps.webhooks.tasks import process_webhook_event_task
```

**Acceptance Criteria:**
- [x] Handlers extracted
- [x] Generic enough for customization
- [x] Documentation added
- [x] Example implementation included

---

### Phase 7: Templates & Static Assets (Day 3-4)
**Goal:** Extract and customize templates and static files

#### Task 7.1: Extract Base Templates
**Source:** `templates/base.html`

**Target:** `templates/base.html`

**Actions:**
1. Copy base.html
2. Remove "NexMenus" branding
3. Update meta tags
4. Generic title structure
5. Keep analytics with environment exclusions

**Modifications:**
```html
<!-- BEFORE -->
<title>{% block title %}NexMenus - Restaurant Website Builder{% endblock %}</title>

<!-- AFTER -->
<title>{% block title %}{{ SITE_NAME|default:"Django SaaS Starter" }}{% endblock %}</title>
```

**Acceptance Criteria:**
- [x] Base template extracted
- [x] Branding removed
- [x] Configurable site name
- [x] Analytics preserved

---

#### Task 7.2: Extract Layout Components
**Source:** `templates/layout/`

**Target:** `templates/layout/`

**Files:**
- `topbar.html` - Navigation bar
- `footer.html` - Footer component
- `sidebar.html` - Sidebar component (if applicable)

**Actions:**
1. Copy component templates
2. Remove domain-specific navigation links
3. Add placeholder links
4. Document customization points

**Acceptance Criteria:**
- [x] Components extracted
- [x] Generic navigation
- [x] Customization documented

---

#### Task 7.3: Extract Error Pages
**Source:** `templates/`

**Target:** `templates/errors/`

**Files:**
- `403.html` - Forbidden
- `404.html` - Not Found
- `429.html` - Rate Limited
- `500.html` - Server Error

**Actions:** Copy as-is (already generic)

**Acceptance Criteria:**
- [x] Error pages copied
- [x] Styling preserved

---

#### Task 7.4: Extract Account Templates
**Source:** `templates/account/`

**Target:** `templates/account/`

**Actions:**
1. Copy customized allauth templates
2. Remove domain-specific messaging
3. Keep styling and structure

**Acceptance Criteria:**
- [x] Account templates copied
- [x] Generic messaging
- [x] Allauth overrides work

---

#### Task 7.5: Create Generic Home/Landing Pages
**Source:** `templates/home.html`, `templates/landing.html`

**Target:**
- `templates/home.html`
- `templates/landing.html`

**Actions:**
1. Copy templates
2. Replace domain-specific content with placeholders
3. Add documentation blocks for customization
4. Keep structure and styling

**Acceptance Criteria:**
- [x] Home page created
- [x] Landing page created
- [x] Placeholder content
- [x] Documentation comments

---

#### Task 7.6: Extract Static Assets
**Source:** `static/`

**Target:** `static/`

**Actions:**
1. Copy favicon files (or create generic/document)
2. Copy generic CSS (exclude domain-specific)
3. Copy generic JavaScript utilities
4. Document what to customize

**Keep:**
- `static/favicon/` - Generic favicon or document generation
- Generic utility CSS/JS
- Framework files (if any)

**Exclude:**
- Domain-specific images
- App-specific JavaScript
- Custom illustrations

**Acceptance Criteria:**
- [x] Generic static files copied
- [x] Favicon handled
- [x] Customization documented

---

### Phase 8: Configuration & URLs (Day 4)
**Goal:** Wire everything together

#### Task 8.1: Create Main URLs Configuration
**Source:** `NexMenus/urls.py`

**Target:** `config/urls.py`

**Actions:**
1. Copy URL structure
2. Remove domain-specific URL includes
3. Keep core patterns (admin, accounts, webhooks, i18n)
4. Add subscription URLs
5. Document where to add custom URLs

**Code:**
```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.conf.urls.static import static
from django.views.generic import TemplateView
from apps.webhooks.handlers import account_webhook_router, connect_webhook_router

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication (django-allauth)
    path('accounts/', include('allauth.urls')),

    # Webhooks
    path('webhooks/stripe/account/', account_webhook_router, name='stripe_account_webhook'),
    path('webhooks/stripe/connect/', connect_webhook_router, name='stripe_connect_webhook'),

    # Internationalization
    path('i18n/', include('django.conf.urls.i18n')),
    path('i18n/setlang/', set_language, name='set_language'),

    # Robots & Sitemap (examples)
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain"
    )),

    # Home page (customize this)
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]

# Internationalized URLs
urlpatterns += i18n_patterns(
    # Subscription management
    path('subscription/', include(('apps.subscription.urls', 'subscription'))),

    # Add your app URLs here
    # path('yourapp/', include('apps.yourapp.urls')),

    prefix_default_language=True,
)

# Development URLs
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Acceptance Criteria:**
- [x] URLs configured
- [x] Domain-specific URLs removed
- [x] Core URLs included
- [x] Documentation added

---

#### Task 8.2: Configure WSGI/ASGI
**Source:** `NexMenus/wsgi.py`, `NexMenus/asgi.py`

**Target:** `config/wsgi.py`, `config/asgi.py`

**Actions:**
1. Copy WSGI configuration
2. Update settings module path
3. Copy ASGI if exists

**Modifications:**
```python
# config/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```

**Acceptance Criteria:**
- [x] WSGI configured
- [x] ASGI configured (if needed)
- [x] Settings module path updated

---

#### Task 8.3: Configure Celery
**Source:** Check for `NexMenus/celery.py`

**Target:** `config/celery.py`

**Actions:**
1. Create Celery app configuration
2. Update settings module reference
3. Add autodiscover_tasks

**Code:**
```python
# config/celery.py
import os
from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load config from Django settings with CELERY namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery setup."""
    print(f'Request: {self.request!r}')
```

**Acceptance Criteria:**
- [x] Celery app created
- [x] Settings loaded
- [x] Autodiscovery configured
- [x] Debug task included

---

### Phase 9: Documentation (Day 4-5)
**Goal:** Create comprehensive documentation

#### Task 9.1: Create Main README
**Target:** `README.md`

**Sections:**
1. Project overview
2. Features list
3. Quick start guide
4. Requirements
5. Installation steps
6. Configuration overview
7. Development workflow
8. Deployment guide
9. Contributing
10. License

**Key Content:**
- What's included
- Technology stack
- How to customize
- Links to detailed docs

**Acceptance Criteria:**
- [x] README created
- [x] All sections complete
- [x] Examples included
- [x] Clear and professional

---

#### Task 9.2: Create Installation Guide
**Target:** `docs/INSTALLATION.md`

**Content:**
```markdown
# Installation Guide

## Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- AWS S3 bucket (for media storage)

## Step-by-Step Installation

### 1. Clone Repository
...

### 2. Create Virtual Environment
...

### 3. Install Dependencies
...

### 4. Environment Configuration
...

### 5. Database Setup
...

### 6. Run Migrations
...

### 7. Create Superuser
...

### 8. Run Development Server
...
```

**Acceptance Criteria:**
- [x] Step-by-step instructions
- [x] All prerequisites listed
- [x] Troubleshooting section
- [x] Platform-specific notes

---

#### Task 9.3: Create Configuration Guide
**Target:** `docs/CONFIGURATION.md`

**Content:**
- All environment variables documented
- Settings files explained
- Feature toggles
- Third-party service setup
- Security considerations

**Acceptance Criteria:**
- [x] All env vars documented
- [x] Examples provided
- [x] Security notes included

---

#### Task 9.4: Create Stripe Setup Guide
**Target:** `docs/STRIPE_SETUP.md`

**Content:**
- Stripe account creation
- API keys configuration
- Webhook setup
- Product/price creation
- Testing with Stripe CLI
- Going to production

**Acceptance Criteria:**
- [x] Complete Stripe setup
- [x] Webhook configuration
- [x] Testing instructions
- [x] Production checklist

---

#### Task 9.5: Create Deployment Guide
**Target:** `docs/DEPLOYMENT.md`

**Content:**
- Heroku deployment
- Environment variables for production
- Database setup (Heroku Postgres)
- Redis setup (Heroku Redis or other)
- S3 configuration
- Celery worker configuration
- Domain & SSL setup
- Post-deployment checklist

**Acceptance Criteria:**
- [x] Heroku instructions complete
- [x] Alternative platforms mentioned
- [x] Security checklist included
- [x] Troubleshooting section

---

#### Task 9.6: Create Customization Guide
**Target:** `docs/CUSTOMIZATION.md`

**Content:**
- How to add new apps
- Extending User model
- Custom subscription plans
- Template customization
- Branding updates
- Adding features

**Acceptance Criteria:**
- [x] Clear examples
- [x] Best practices
- [x] Common patterns
- [x] Code snippets

---

#### Task 9.7: Create Environment Template
**Target:** `.env.example`

**Content:**
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ENV=development
ALLOWED_HOSTS=localhost,127.0.0.1
BASE_URL=http://localhost:8000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Stripe
STRIPE_API_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_ACCOUNT_WEBHOOK_SECRET=whsec_...
STRIPE_CONNECT_WEBHOOK_SECRET=whsec_...

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# reCAPTCHA
RECAPTCHA_PUBLIC_KEY=your-site-key
RECAPTCHA_PRIVATE_KEY=your-secret-key
DISABLE_RECAPTCHA=False

# Sentry (optional)
SENTRY_DSN=

# Feature Flags
MAINTENANCE_MODE=False
```

**Acceptance Criteria:**
- [x] All variables included
- [x] Comments explain each
- [x] Example values provided
- [x] Optional variables marked

---

### Phase 10: Testing & Validation (Day 5-6)
**Goal:** Ensure everything works

#### Task 10.1: Generate Migrations
**Actions:**
1. Delete all migrations except `__init__.py` in each app
2. Run `python manage.py makemigrations`
3. Verify migrations created correctly
4. Run `python manage.py migrate`
5. Check database schema

**Acceptance Criteria:**
- [x] Clean migrations generated
- [x] No migration conflicts
- [x] Database created successfully
- [x] All tables present

---

#### Task 10.2: Create Superuser & Test Admin
**Actions:**
1. Run `python manage.py createsuperuser`
2. Access `/admin/`
3. Verify all models registered
4. Test maintenance mode toggle
5. Test user management

**Acceptance Criteria:**
- [x] Superuser created
- [x] Admin accessible
- [x] All apps visible
- [x] CRUD operations work

---

#### Task 10.3: Test Authentication Flow
**Actions:**
1. Test signup with reCAPTCHA
2. Test login
3. Test logout
4. Test password reset
5. Test rate limiting

**Acceptance Criteria:**
- [x] Signup works
- [x] Login works
- [x] Rate limiting active
- [x] Email templates render

---

#### Task 10.4: Test Subscription Flow
**Actions:**
1. Configure Stripe test keys
2. Test subscription creation
3. Test webhook handling
4. Test subscription status display
5. Test cancellation

**Acceptance Criteria:**
- [x] Can create subscription
- [x] Webhooks processed
- [x] Status updates correctly
- [x] UI shows correct data

---

#### Task 10.5: Test Maintenance Mode
**Actions:**
1. Enable via admin
2. Test non-staff access (should see maintenance page)
3. Test staff access (should bypass)
4. Test excluded URLs
5. Disable via admin

**Acceptance Criteria:**
- [x] Maintenance page shows
- [x] Staff can bypass
- [x] Excluded paths work
- [x] Toggle works

---

#### Task 10.6: Test Celery Tasks
**Actions:**
1. Start Redis
2. Start Celery worker
3. Trigger async task (e.g., webhook processing)
4. Verify task execution
5. Check logs

**Acceptance Criteria:**
- [x] Celery connects to Redis
- [x] Tasks execute
- [x] Results stored
- [x] No errors

---

#### Task 10.7: Test S3 Integration
**Actions:**
1. Configure S3 credentials
2. Upload test file via admin
3. Verify file in S3
4. Test file deletion
5. Verify deletion in S3

**Acceptance Criteria:**
- [x] Files upload to S3
- [x] Files accessible
- [x] Deletion works
- [x] Permissions correct

---

#### Task 10.8: Run Full Test Suite
**Actions:**
1. Set up pytest
2. Write basic tests for each app
3. Run test suite
4. Fix any failures
5. Achieve minimum coverage

**Test Areas:**
- User model
- Subscription models
- Maintenance mode
- Middleware
- Utilities

**Acceptance Criteria:**
- [x] All tests pass
- [x] Core functionality covered
- [x] No critical bugs

---

### Phase 11: Polish & Release (Day 6)
**Goal:** Final touches and prepare for release

#### Task 11.1: Code Cleanup
**Actions:**
1. Remove commented code
2. Fix linting issues
3. Standardize docstrings
4. Remove debug statements
5. Verify no hardcoded secrets

**Acceptance Criteria:**
- [x] Clean code
- [x] Consistent style
- [x] No secrets committed
- [x] Linting passes

---

#### Task 11.2: Documentation Review
**Actions:**
1. Proofread all documentation
2. Verify all links work
3. Test installation steps
4. Update screenshots if needed
5. Add changelog/version

**Acceptance Criteria:**
- [x] Docs accurate
- [x] No broken links
- [x] Clear instructions
- [x] Professional quality

---

#### Task 11.3: Create Demo Content
**Actions:**
1. Create sample data script
2. Generate demo users
3. Create example subscription plans
4. Add sample content

**Acceptance Criteria:**
- [x] Demo script created
- [x] Sample data available
- [x] Easy to populate
- [x] Easy to clear

---

#### Task 11.4: License & Attribution
**Actions:**
1. Add LICENSE file (MIT suggested)
2. Add attribution to README
3. Credit dependencies
4. Add contributing guidelines

**Acceptance Criteria:**
- [x] License added
- [x] Attributions complete
- [x] Contributing guide created

---

#### Task 11.5: GitHub Release Preparation
**Actions:**
1. Clean git history
2. Tag version (v1.0.0)
3. Write release notes
4. Create GitHub repo description
5. Add topics/tags

**Acceptance Criteria:**
- [x] Git cleaned
- [x] Version tagged
- [x] Release notes written
- [x] Repo ready for public

---

## File Migration Checklist

### Files to Copy As-Is ✅

```
✅ NexMenus/settings/base.py → config/settings/base.py (with modifications)
✅ NexMenus/settings/development.py → config/settings/development.py
✅ NexMenus/settings/qa.py → config/settings/qa.py
✅ NexMenus/settings/prod.py → config/settings/prod.py
✅ NexMenus/common_utils.py → apps/core/utils.py
✅ subscription/models.py → apps/subscription/models.py
✅ subscription/enums.py → apps/subscription/enums.py
✅ subscription/utils.py → apps/subscription/utils.py
✅ maintenance/ → apps/maintenance/ (entire app)
✅ accounts/forms.py → apps/accounts/forms.py
✅ requirements.txt → requirements.txt (with review)
```

### Files to Extract & Modify ⚠️

```
⚠️ menu/models.py (User + BaseModel only) → apps/accounts/models.py + apps/core/models.py
⚠️ menu/utils.py (S3 functions only) → apps/core/storage.py
⚠️ NexMenus/middleware.py → apps/core/middleware.py
⚠️ NexMenus/urls.py → config/urls.py (simplified)
⚠️ webhooks/handlers.py → apps/webhooks/handlers.py
⚠️ templates/base.html → templates/base.html (rebranded)
⚠️ templates/layout/* → templates/layout/* (generic links)
```

### Files to Create New 🆕

```
🆕 apps/core/models.py (BaseModel)
🆕 apps/core/storage.py (S3 utilities)
🆕 apps/core/context_processors.py
🆕 apps/accounts/models.py (User model)
🆕 apps/webhooks/models.py (WebhookEvent)
🆕 config/celery.py
🆕 README.md
🆕 docs/INSTALLATION.md
🆕 docs/CONFIGURATION.md
🆕 docs/DEPLOYMENT.md
🆕 docs/STRIPE_SETUP.md
🆕 docs/CUSTOMIZATION.md
🆕 .env.example
🆕 LICENSE
```

### Files to Exclude ❌

```
❌ menu/ (except User, BaseModel)
❌ ordering/ (entire app)
❌ catalog/ (entire app)
❌ blog/ (entire app)
❌ test_tools/ (entire app)
❌ onboarding/ (entire app)
❌ legal/ (keep structure, replace content)
❌ Domain-specific templates
❌ Domain-specific static assets
❌ Domain-specific management commands
```

---

## Testing & Validation

### Manual Testing Checklist

#### Core Functionality
- [ ] Project starts without errors
- [ ] Admin accessible
- [ ] Static files load
- [ ] Templates render
- [ ] Database connections work

#### Authentication
- [ ] Signup works
- [ ] Login works
- [ ] Logout works
- [ ] Password reset works
- [ ] reCAPTCHA displays
- [ ] Rate limiting activates
- [ ] Email sending works (or logs in dev)

#### Subscriptions
- [ ] Can view subscription page
- [ ] Stripe checkout works (test mode)
- [ ] Webhooks process correctly
- [ ] Subscription status updates
- [ ] Customer object created
- [ ] Can cancel subscription

#### Maintenance Mode
- [ ] Can enable via admin
- [ ] Non-staff see maintenance page
- [ ] Staff bypass maintenance mode
- [ ] Can disable via admin
- [ ] Custom message displays

#### Infrastructure
- [ ] Celery worker starts
- [ ] Redis connection works
- [ ] S3 uploads work
- [ ] S3 deletion works
- [ ] Migrations run cleanly
- [ ] Different environments load correct settings

#### Internationalization
- [ ] Language switching works
- [ ] Translations load
- [ ] i18n URLs work
- [ ] Locale middleware functions

---

## Success Metrics

### Code Quality
- ✅ No hardcoded credentials
- ✅ All sensitive data in environment variables
- ✅ Proper error handling throughout
- ✅ Consistent code style
- ✅ Comprehensive docstrings

### Documentation
- ✅ Complete installation guide
- ✅ Environment variables documented
- ✅ Deployment instructions clear
- ✅ Customization guide helpful
- ✅ Stripe setup documented

### Functionality
- ✅ Authentication flow complete
- ✅ Subscription management working
- ✅ Maintenance mode functional
- ✅ Webhooks processing
- ✅ Async tasks executing
- ✅ File storage working

### Developer Experience
- ✅ Quick start under 15 minutes
- ✅ Clear project structure
- ✅ Easy to customize
- ✅ Well-commented code
- ✅ Helpful error messages

---

## Post-Extraction Tasks

### Repository Setup
1. Create GitHub repository
2. Push initial code
3. Configure GitHub settings
4. Add repository description
5. Add topics: django, saas, boilerplate, stripe, celery
6. Enable discussions
7. Add issue templates
8. Configure branch protection

### Community
1. Create CONTRIBUTING.md
2. Create CODE_OF_CONDUCT.md
3. Set up issue templates
4. Create PR template
5. Add changelog

### Marketing
1. Create demo site
2. Record demo video
3. Write blog post
4. Share on social media
5. Submit to awesome lists

---

## Maintenance Plan

### Version 1.0.0 (Initial Release)
- Core infrastructure
- Basic documentation
- Essential features

### Version 1.1.0 (Planned)
- Enhanced documentation
- More examples
- Video tutorials
- Docker support

### Version 1.2.0 (Planned)
- Additional payment providers
- More authentication options
- Enhanced admin dashboard
- API authentication

---

## Notes for Execution

### Key Decisions Made
1. **Project Name**: `django-saas-starter` (configurable)
2. **Package Name**: `config` instead of `NexMenus`
3. **Apps Directory**: All apps in `apps/` package
4. **License**: MIT (recommended for boilerplate)
5. **Python Version**: 3.11+ requirement
6. **Django Version**: 5.1.1

### Assumptions
- PostgreSQL as primary database
- Redis for caching and Celery
- AWS S3 for media storage
- Heroku as primary deployment target (but documented for others)
- Stripe for subscriptions
- Email-based authentication (no social login by default)

### Customization Points
All customization points should be clearly documented:
1. Branding (site name, logo, colors)
2. Subscription plans
3. Email templates
4. Home/landing pages
5. Navigation structure
6. Additional apps

---

## Timeline Summary

| Phase | Duration | Key Deliverables |
|-------|----------|------------------|
| 1. Project Init | 0.5 day | Django project, settings structure |
| 2. Core Infrastructure | 1 day | BaseModel, utils, middleware |
| 3. User & Auth | 0.5 day | User model, auth forms |
| 4. Subscriptions | 0.5 day | Stripe integration |
| 5. Maintenance | 0.25 day | Maintenance mode |
| 6. Webhooks | 0.5 day | Webhook infrastructure |
| 7. Templates | 0.75 day | UI templates |
| 8. Config & URLs | 0.5 day | URL routing, WSGI |
| 9. Documentation | 1 day | All docs |
| 10. Testing | 1 day | QA and validation |
| 11. Polish | 0.5 day | Final touches |
| **Total** | **~6 days** | Production-ready SaaS boilerplate |

---

## Conclusion

This extraction plan provides a complete roadmap for converting NexMenus into a reusable Django SaaS boilerplate. The resulting project will be:

- **Production-ready**: Tested infrastructure and security
- **Well-documented**: Comprehensive guides for setup and customization
- **Highly reusable**: 60-70% of codebase is generic
- **Developer-friendly**: Clear structure and conventions
- **Scalable**: Built with growth in mind (Celery, Redis, S3)
- **Secure**: Industry best practices implemented

The extraction preserves all the valuable infrastructure while removing domain-specific logic, creating a solid foundation for any Django-based SaaS application.
