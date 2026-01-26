"""
Tests for the core app.
"""
import os
from unittest import mock
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from apps.core.utils import get_env_int, get_env_float, get_env_number, get_env_bool
from apps.core.context_processors import environment, recaptcha, user_subscription

User = get_user_model()


class UtilsTests(TestCase):
    """Tests for core utility functions."""

    def test_get_env_int_returns_int(self):
        """Test get_env_int returns integer from environment."""
        with mock.patch.dict(os.environ, {'TEST_INT': '42'}):
            result = get_env_int('TEST_INT')
            self.assertEqual(result, 42)
            self.assertIsInstance(result, int)

    def test_get_env_int_returns_default(self):
        """Test get_env_int returns default when key missing."""
        result = get_env_int('NONEXISTENT_KEY', 100)
        self.assertEqual(result, 100)

    def test_get_env_int_returns_default_on_invalid(self):
        """Test get_env_int returns default on invalid value."""
        with mock.patch.dict(os.environ, {'TEST_INT': 'not_a_number'}):
            result = get_env_int('TEST_INT', 50)
            self.assertEqual(result, 50)

    def test_get_env_float_returns_float(self):
        """Test get_env_float returns float from environment."""
        with mock.patch.dict(os.environ, {'TEST_FLOAT': '3.14'}):
            result = get_env_float('TEST_FLOAT')
            self.assertAlmostEqual(result, 3.14)
            self.assertIsInstance(result, float)

    def test_get_env_float_returns_default(self):
        """Test get_env_float returns default when key missing."""
        result = get_env_float('NONEXISTENT_KEY', 2.5)
        self.assertEqual(result, 2.5)

    def test_get_env_number_returns_int(self):
        """Test get_env_number returns int when value is whole number."""
        with mock.patch.dict(os.environ, {'TEST_NUM': '100'}):
            result = get_env_number('TEST_NUM')
            self.assertEqual(result, 100)
            self.assertIsInstance(result, int)

    def test_get_env_number_returns_float(self):
        """Test get_env_number returns float when value has decimal."""
        with mock.patch.dict(os.environ, {'TEST_NUM': '3.14'}):
            result = get_env_number('TEST_NUM')
            self.assertAlmostEqual(result, 3.14)
            self.assertIsInstance(result, float)

    def test_get_env_bool_true_values(self):
        """Test get_env_bool recognizes true values."""
        for value in ['true', 'True', 'TRUE', 'yes', 'YES', '1', 'on', 'ON']:
            with mock.patch.dict(os.environ, {'TEST_BOOL': value}):
                result = get_env_bool('TEST_BOOL')
                self.assertTrue(result, f"Expected True for '{value}'")

    def test_get_env_bool_false_values(self):
        """Test get_env_bool returns False for other values."""
        for value in ['false', 'False', 'no', '0', 'off', 'random']:
            with mock.patch.dict(os.environ, {'TEST_BOOL': value}):
                result = get_env_bool('TEST_BOOL')
                self.assertFalse(result, f"Expected False for '{value}'")

    def test_get_env_bool_returns_default(self):
        """Test get_env_bool returns default when key missing."""
        result = get_env_bool('NONEXISTENT_KEY', True)
        self.assertTrue(result)


class ContextProcessorsTests(TestCase):
    """Tests for context processors."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_environment_processor(self):
        """Test environment context processor returns expected keys."""
        request = self.factory.get('/')
        context = environment(request)
        self.assertIn('DEBUG', context)
        self.assertIn('ENV', context)
        self.assertIn('BASE_URL', context)

    def test_recaptcha_processor(self):
        """Test recaptcha context processor returns expected keys."""
        request = self.factory.get('/')
        context = recaptcha(request)
        self.assertIn('RECAPTCHA_SITE_KEY', context)
        self.assertIn('RECAPTCHA_ENABLED', context)

    def test_user_subscription_anonymous_user(self):
        """Test user_subscription returns empty dict for anonymous users."""
        request = self.factory.get('/')
        request.user = type('AnonymousUser', (), {'is_authenticated': False})()
        context = user_subscription(request)
        self.assertEqual(context, {})

    def test_user_subscription_authenticated_user(self):
        """Test user_subscription returns data for authenticated users."""
        user = User.objects.create_user(
            username='subtest',
            email='subtest@example.com',
            password='testpass123'
        )
        request = self.factory.get('/')
        request.user = user
        context = user_subscription(request)
        self.assertIn('user_subscription', context)
        self.assertIn('has_active_subscription', context)


class MiddlewareTests(TestCase):
    """Tests for middleware classes."""

    def test_middleware_imports(self):
        """Test that all middleware classes can be imported."""
        from apps.core.middleware import (
            MaintenanceModeMiddleware,
            TranslationDebugMiddleware,
            FirebaseMiddleware
        )
        self.assertIsNotNone(MaintenanceModeMiddleware)
        self.assertIsNotNone(TranslationDebugMiddleware)
        self.assertIsNotNone(FirebaseMiddleware)

    def test_firebase_middleware_returns_204_for_service_worker(self):
        """Test FirebaseMiddleware returns 204 for firebase service worker."""
        from apps.core.middleware import FirebaseMiddleware

        def get_response(request):
            from django.http import HttpResponse
            return HttpResponse('OK')

        middleware = FirebaseMiddleware(get_response)
        factory = RequestFactory()
        request = factory.get('/firebase-messaging-sw.js')
        response = middleware(request)
        self.assertEqual(response.status_code, 204)

    def test_firebase_middleware_passes_through_other_requests(self):
        """Test FirebaseMiddleware passes through normal requests."""
        from apps.core.middleware import FirebaseMiddleware

        def get_response(request):
            from django.http import HttpResponse
            return HttpResponse('OK', status=200)

        middleware = FirebaseMiddleware(get_response)
        factory = RequestFactory()
        request = factory.get('/some/other/path/')
        response = middleware(request)
        self.assertEqual(response.status_code, 200)


class StorageTests(TestCase):
    """Tests for S3 storage utilities."""

    def test_storage_functions_exist(self):
        """Test that storage functions can be imported."""
        from apps.core.storage import get_s3_client, delete_s3_objects
        self.assertIsNotNone(get_s3_client)
        self.assertIsNotNone(delete_s3_objects)

    def test_delete_s3_objects_requires_prefix(self):
        """Test delete_s3_objects returns False without prefix."""
        from apps.core.storage import delete_s3_objects
        result = delete_s3_objects(prefix=None)
        self.assertFalse(result)

        result = delete_s3_objects(prefix='')
        self.assertFalse(result)
