"""
Tests for the maintenance app.
"""
from django.test import TestCase, override_settings
from django.core.cache import cache
from apps.maintenance.models import MaintenanceMode


# Use a local memory cache for tests to avoid Redis dependency
TEST_CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


@override_settings(CACHES=TEST_CACHES)
class MaintenanceModeModelTests(TestCase):
    """Tests for the MaintenanceMode singleton model."""

    def setUp(self):
        """Clear cache before each test."""
        cache.clear()

    def test_get_instance_creates_singleton(self):
        """Test get_instance creates a singleton instance."""
        instance1 = MaintenanceMode.get_instance()
        instance2 = MaintenanceMode.get_instance()
        self.assertEqual(instance1.pk, instance2.pk)

    def test_maintenance_mode_default_inactive(self):
        """Test maintenance mode is inactive by default."""
        instance = MaintenanceMode.get_instance()
        self.assertFalse(instance.is_active)

    def test_maintenance_mode_has_message(self):
        """Test maintenance mode has a message field."""
        instance = MaintenanceMode.get_instance()
        self.assertTrue(hasattr(instance, 'message'))
        self.assertIsNotNone(instance.message)

    def test_maintenance_mode_can_be_activated(self):
        """Test maintenance mode can be activated."""
        instance = MaintenanceMode.get_instance()
        instance.is_active = True
        instance.message = "Test maintenance message"
        instance.save()

        # Retrieve fresh instance
        fresh_instance = MaintenanceMode.get_instance()
        self.assertTrue(fresh_instance.is_active)
        self.assertEqual(fresh_instance.message, "Test maintenance message")

    def test_is_maintenance_mode_active_class_method(self):
        """Test class method returns correct status."""
        # Ensure maintenance is off
        instance = MaintenanceMode.get_instance()
        instance.is_active = False
        instance.save()

        self.assertFalse(MaintenanceMode.is_maintenance_mode_active())

        # Turn on maintenance
        instance.is_active = True
        instance.save()

        # Clear cache to ensure fresh read
        cache.clear()
        self.assertTrue(MaintenanceMode.is_maintenance_mode_active())

    def test_singleton_prevents_multiple_records(self):
        """Test only one MaintenanceMode record can exist."""
        instance1 = MaintenanceMode.get_instance()
        count = MaintenanceMode.objects.count()
        self.assertEqual(count, 1)

        # Attempting to get instance again should return same record
        instance2 = MaintenanceMode.get_instance()
        count_after = MaintenanceMode.objects.count()
        self.assertEqual(count_after, 1)
        self.assertEqual(instance1.pk, instance2.pk)

    def test_str_representation(self):
        """Test string representation of MaintenanceMode."""
        instance = MaintenanceMode.get_instance()
        str_repr = str(instance)
        self.assertIsInstance(str_repr, str)
        self.assertIn('Maintenance Mode', str_repr)
        self.assertIn('INACTIVE', str_repr)

        # Test active status string
        instance.is_active = True
        instance.save()
        str_repr = str(instance)
        self.assertIn('ACTIVE', str_repr)

    def test_cache_is_updated_on_save(self):
        """Test that cache is updated when model is saved."""
        instance = MaintenanceMode.get_instance()
        instance.is_active = True
        instance.save()

        # Check cache was updated
        cached_status = cache.get('maintenance_mode_active')
        self.assertTrue(cached_status)

        instance.is_active = False
        instance.save()

        cached_status = cache.get('maintenance_mode_active')
        self.assertFalse(cached_status)
