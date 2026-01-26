"""
Tests for the webhooks app.
"""
from django.test import TestCase
from apps.webhooks.models import WebhookEvent, WebhookEventStatus


class WebhookEventStatusEnumTests(TestCase):
    """Tests for the WebhookEventStatus enum."""

    def test_webhook_event_status_values(self):
        """Test WebhookEventStatus enum has expected values."""
        self.assertEqual(WebhookEventStatus.RECEIVED, 'received')
        self.assertEqual(WebhookEventStatus.PROCESSING, 'processing')
        self.assertEqual(WebhookEventStatus.PROCESSED, 'processed')
        self.assertEqual(WebhookEventStatus.FAILED, 'failed')


class WebhookEventModelTests(TestCase):
    """Tests for the WebhookEvent model."""

    def test_create_webhook_event(self):
        """Test creating a webhook event."""
        event = WebhookEvent.objects.create(
            event_id='evt_test123',
            provider='stripe',
            payload={'test': 'data'}
        )
        self.assertEqual(event.event_id, 'evt_test123')
        self.assertEqual(event.provider, 'stripe')
        self.assertEqual(event.payload, {'test': 'data'})

    def test_webhook_event_default_status(self):
        """Test webhook event defaults to received status."""
        event = WebhookEvent.objects.create(
            event_id='evt_pending123',
            provider='test',
            payload={}
        )
        self.assertEqual(event.status, WebhookEventStatus.RECEIVED)

    def test_webhook_event_uuid_primary_key(self):
        """Test WebhookEvent uses UUID primary key."""
        import uuid
        event = WebhookEvent.objects.create(
            event_id='evt_uuid123',
            provider='test',
            payload={}
        )
        self.assertIsInstance(event.id, uuid.UUID)

    def test_mark_as_processing(self):
        """Test mark_as_processing method."""
        event = WebhookEvent.objects.create(
            event_id='evt_processing123',
            provider='test',
            payload={}
        )
        event.mark_as_processing()
        event.refresh_from_db()
        self.assertEqual(event.status, WebhookEventStatus.PROCESSING)

    def test_mark_as_processed(self):
        """Test mark_as_processed method."""
        event = WebhookEvent.objects.create(
            event_id='evt_processed123',
            provider='test',
            payload={}
        )
        event.mark_as_processed()
        event.refresh_from_db()
        self.assertEqual(event.status, WebhookEventStatus.PROCESSED)
        self.assertIsNotNone(event.processed_at)

    def test_mark_as_failed(self):
        """Test mark_as_failed method."""
        event = WebhookEvent.objects.create(
            event_id='evt_failed123',
            provider='test',
            payload={}
        )
        event.mark_as_failed(error_message='Test error')
        event.refresh_from_db()
        self.assertEqual(event.status, WebhookEventStatus.FAILED)
        self.assertEqual(event.error_message, 'Test error')
        self.assertEqual(event.retry_count, 1)

    def test_webhook_event_timestamps(self):
        """Test WebhookEvent has received_at timestamp."""
        event = WebhookEvent.objects.create(
            event_id='evt_time123',
            provider='test',
            payload={}
        )
        self.assertIsNotNone(event.received_at)

    def test_webhook_event_str(self):
        """Test WebhookEvent string representation."""
        event = WebhookEvent.objects.create(
            event_id='evt_str123',
            provider='stripe',
            payload={}
        )
        str_repr = str(event)
        self.assertIn('stripe', str_repr)
        self.assertIn('evt_str123', str_repr)

    def test_webhook_event_unique_together(self):
        """Test provider + event_id uniqueness constraint."""
        WebhookEvent.objects.create(
            event_id='evt_unique123',
            provider='stripe',
            payload={}
        )
        # Creating a duplicate should raise an error
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            WebhookEvent.objects.create(
                event_id='evt_unique123',
                provider='stripe',
                payload={}
            )


class WebhookHandlersTests(TestCase):
    """Tests for webhook handler functions."""

    def test_handlers_exist(self):
        """Test webhook handlers can be imported."""
        from apps.webhooks.handlers import (
            account_webhook_router,
            connect_webhook_router
        )
        self.assertIsNotNone(account_webhook_router)
        self.assertIsNotNone(connect_webhook_router)
