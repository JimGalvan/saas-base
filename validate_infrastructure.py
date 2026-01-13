#!/usr/bin/env python
"""
Infrastructure Validation Script for Django SaaS Starter
Tests all core components to ensure proper extraction and configuration.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Test results tracking
passed = []
failed = []


def test(name, func):
    """Run a test and track results."""
    try:
        func()
        passed.append(name)
        print(f"[PASS] {name}")
        return True
    except Exception as e:
        failed.append((name, str(e)))
        print(f"[FAIL] {name}: {str(e)}")
        return False


# ============================================================================
# Test 1: Model Imports
# ============================================================================

def test_model_imports():
    """Test that all models can be imported."""
    from apps.accounts.models import User
    from apps.subscription.models import Customer, Subscription
    from apps.maintenance.models import MaintenanceMode
    from apps.webhooks.models import WebhookEvent
    from apps.core.models import BaseModel
    assert User is not None
    assert Customer is not None
    assert Subscription is not None
    assert MaintenanceMode is not None
    assert WebhookEvent is not None
    assert BaseModel is not None


test("Model Imports", test_model_imports)


# ============================================================================
# Test 2: User Model
# ============================================================================

def test_user_model():
    """Test User model has required methods."""
    from apps.accounts.models import User
    assert hasattr(User, 'has_active_subscription')
    assert hasattr(User, 'has_ever_had_subscription')
    # Check UUID primary key
    from django.db import models
    assert isinstance(User._meta.get_field('id'), models.UUIDField)


test("User Model Methods", test_user_model)


# ============================================================================
# Test 3: BaseModel
# ============================================================================

def test_basemodel():
    """Test BaseModel has timestamps."""
    from apps.core.models import BaseModel
    from apps.subscription.models import Customer
    # Customer inherits from BaseModel
    assert hasattr(Customer, 'created_at')
    assert hasattr(Customer, 'updated_at')
    assert hasattr(Customer, 'id')


test("BaseModel Abstract Class", test_basemodel)


# ============================================================================
# Test 4: Subscription Enums
# ============================================================================

def test_subscription_enums():
    """Test subscription enums are defined."""
    from apps.subscription.enums import PlanType, SubscriptionStatus
    assert hasattr(PlanType, 'FREE')
    assert hasattr(PlanType, 'PLUS')
    assert hasattr(SubscriptionStatus, 'ACTIVE')
    assert hasattr(SubscriptionStatus, 'CANCELED')


test("Subscription Enums", test_subscription_enums)


# ============================================================================
# Test 5: Subscription Model
# ============================================================================

def test_subscription_model():
    """Test Subscription model has required properties."""
    from apps.subscription.models import Subscription
    assert hasattr(Subscription, 'is_active')
    assert hasattr(Subscription, 'plan')
    assert hasattr(Subscription, 'status')


test("Subscription Model", test_subscription_model)


# ============================================================================
# Test 6: Maintenance Mode
# ============================================================================

def test_maintenance_mode():
    """Test MaintenanceMode singleton (requires Redis for caching)."""
    from apps.maintenance.models import MaintenanceMode
    try:
        instance = MaintenanceMode.get_instance()
        assert instance is not None
        assert hasattr(instance, 'is_active')
        assert hasattr(instance, 'message')
        # Test class method
        is_active = MaintenanceMode.is_maintenance_mode_active()
        assert isinstance(is_active, bool)
    except Exception as e:
        # Redis not running is acceptable for development
        # Just verify the model class exists
        if "redis" in str(e).lower() or "connection" in str(e).lower():
            assert hasattr(MaintenanceMode, 'get_instance')
            assert hasattr(MaintenanceMode, 'is_maintenance_mode_active')
        else:
            raise


test("Maintenance Mode Singleton", test_maintenance_mode)


# ============================================================================
# Test 7: Webhook Model
# ============================================================================

def test_webhook_model():
    """Test WebhookEvent model has required methods."""
    from apps.webhooks.models import WebhookEvent
    assert hasattr(WebhookEvent, 'mark_as_processed')
    assert hasattr(WebhookEvent, 'mark_as_processing')
    assert hasattr(WebhookEvent, 'mark_as_failed')


test("Webhook Event Model", test_webhook_model)


# ============================================================================
# Test 8: Admin Registration
# ============================================================================

def test_admin_registration():
    """Test all models are registered in admin."""
    from django.contrib import admin
    from apps.accounts.models import User
    from apps.subscription.models import Customer, Subscription
    from apps.maintenance.models import MaintenanceMode
    from apps.webhooks.models import WebhookEvent

    assert admin.site.is_registered(User)
    assert admin.site.is_registered(Customer)
    assert admin.site.is_registered(Subscription)
    assert admin.site.is_registered(MaintenanceMode)
    assert admin.site.is_registered(WebhookEvent)


test("Admin Registration", test_admin_registration)


# ============================================================================
# Test 9: Forms
# ============================================================================

def test_forms():
    """Test authentication forms exist."""
    from apps.accounts.forms import CaptchaSignupForm, CustomLoginForm
    assert CaptchaSignupForm is not None
    assert CustomLoginForm is not None


test("Authentication Forms", test_forms)


# ============================================================================
# Test 10: Middleware
# ============================================================================

def test_middleware():
    """Test middleware classes exist."""
    from apps.core.middleware import (
        MaintenanceModeMiddleware,
        TranslationDebugMiddleware,
        FirebaseMiddleware
    )
    assert MaintenanceModeMiddleware is not None
    assert TranslationDebugMiddleware is not None
    assert FirebaseMiddleware is not None


test("Middleware Classes", test_middleware)


# ============================================================================
# Test 11: Context Processors
# ============================================================================

def test_context_processors():
    """Test context processors exist."""
    from apps.core.context_processors import (
        environment,
        recaptcha,
        user_subscription
    )
    assert environment is not None
    assert recaptcha is not None
    assert user_subscription is not None


test("Context Processors", test_context_processors)


# ============================================================================
# Test 12: S3 Storage
# ============================================================================

def test_s3_storage():
    """Test S3 utilities exist."""
    from apps.core.storage import get_s3_client, delete_s3_objects
    assert get_s3_client is not None
    assert delete_s3_objects is not None


test("S3 Storage Utilities", test_s3_storage)


# ============================================================================
# Test 13: Core Utils
# ============================================================================

def test_core_utils():
    """Test core utility functions."""
    from apps.core.utils import (
        get_env_int,
        get_env_float,
        get_env_number,
        get_env_bool
    )
    assert get_env_int is not None
    assert get_env_float is not None
    assert get_env_number is not None
    assert get_env_bool is not None


test("Core Utilities", test_core_utils)


# ============================================================================
# Test 14: Subscription Utils
# ============================================================================

def test_subscription_utils():
    """Test subscription utility functions."""
    from apps.subscription.utils import (
        sync_subscription_status_and_plan,
        get_plan_type,
        is_subscription_not_active
    )
    assert sync_subscription_status_and_plan is not None
    assert get_plan_type is not None
    assert is_subscription_not_active is not None


test("Subscription Utilities", test_subscription_utils)


# ============================================================================
# Test 15: URL Configuration
# ============================================================================

def test_url_configuration():
    """Test URL patterns are configured."""
    from django.urls import reverse
    from django.urls.exceptions import NoReverseMatch

    # Test that admin URL exists
    try:
        admin_url = reverse('admin:index')
        assert admin_url == '/admin/'
    except NoReverseMatch:
        raise AssertionError("Admin URL not configured")

    # Test allauth URLs
    try:
        login_url = reverse('account_login')
        assert '/accounts/login/' in login_url
    except NoReverseMatch:
        raise AssertionError("Allauth URLs not configured")


test("URL Configuration", test_url_configuration)


# ============================================================================
# Test 16: Settings Configuration
# ============================================================================

def test_settings():
    """Test settings are properly configured."""
    from django.conf import settings

    # Check AUTH_USER_MODEL
    assert settings.AUTH_USER_MODEL == 'accounts.User'

    # Check installed apps
    assert 'apps.accounts' in settings.INSTALLED_APPS
    assert 'apps.subscription' in settings.INSTALLED_APPS
    assert 'apps.maintenance' in settings.INSTALLED_APPS
    assert 'apps.webhooks' in settings.INSTALLED_APPS
    assert 'apps.core' in settings.INSTALLED_APPS

    # Check middleware
    middleware_str = ''.join(settings.MIDDLEWARE)
    assert 'MaintenanceModeMiddleware' in middleware_str

    # Check context processors
    for template_engine in settings.TEMPLATES:
        if template_engine['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
            context_processors = template_engine['OPTIONS']['context_processors']
            context_processors_str = ''.join(context_processors)
            assert 'apps.core.context_processors.environment' in context_processors_str
            assert 'apps.core.context_processors.recaptcha' in context_processors_str


test("Settings Configuration", test_settings)


# ============================================================================
# Test 17: Database Connection
# ============================================================================

def test_database_connection():
    """Test database connection works."""
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result == (1,)


test("Database Connection", test_database_connection)


# ============================================================================
# Test 18: Migrations Applied
# ============================================================================

def test_migrations_applied():
    """Test all migrations are applied."""
    from django.db import connection
    from django.db.migrations.recorder import MigrationRecorder
    recorder = MigrationRecorder(connection)
    applied = recorder.applied_migrations()

    # Check key apps have migrations
    app_migrations = {migration[0] for migration in applied}
    assert 'accounts' in app_migrations
    assert 'subscription' in app_migrations
    assert 'maintenance' in app_migrations
    assert 'webhooks' in app_migrations


test("Migrations Applied", test_migrations_applied)


# ============================================================================
# Test 19: Allauth Adapter
# ============================================================================

def test_allauth_adapter():
    """Test allauth adapter exists."""
    try:
        from apps.accounts.adapters import AccountAdapter
        assert AccountAdapter is not None
    except ImportError:
        # Adapter is optional
        pass


test("Allauth Adapter (Optional)", test_allauth_adapter)


# ============================================================================
# Test 20: Webhook Handlers
# ============================================================================

def test_webhook_handlers():
    """Test webhook handlers exist."""
    from apps.webhooks.handlers import (
        account_webhook_router,
        connect_webhook_router
    )
    assert account_webhook_router is not None
    assert connect_webhook_router is not None


test("Webhook Handlers", test_webhook_handlers)


# ============================================================================
# Results Summary
# ============================================================================

print("\n" + "=" * 70)
print(f"VALIDATION RESULTS")
print("=" * 70)
print(f"[+] Passed: {len(passed)}/{len(passed) + len(failed)}")
if failed:
    print(f"[-] Failed: {len(failed)}/{len(passed) + len(failed)}")
    print("\nFailed Tests:")
    for name, error in failed:
        print(f"  - {name}: {error}")
    sys.exit(1)
else:
    print(f"\n[SUCCESS] All tests passed! Django SaaS Starter is properly configured.")
    print(f"\nNext steps:")
    print(f"  1. Create a superuser: python manage.py createsuperuser")
    print(f"  2. Start the development server: python manage.py runserver")
    print(f"  3. Visit http://localhost:8000/admin/ to test the admin interface")
    print(f"  4. Visit http://localhost:8000 to see the landing page")
    sys.exit(0)
