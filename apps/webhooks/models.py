"""
Webhook models for Django SaaS Starter.

This module provides models for storing and tracking webhook events
from external services like Stripe for asynchronous processing.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class WebhookEventStatus(models.TextChoices):
    """
    Status choices for webhook event processing.

    Tracks the lifecycle of a webhook event from receipt to completion.
    """
    RECEIVED = 'received', _('Received')
    PROCESSING = 'processing', _('Processing')
    PROCESSED = 'processed', _('Processed')
    FAILED = 'failed', _('Failed')


class WebhookEvent(models.Model):
    """
    Stores incoming webhook events for asynchronous processing.

    This model captures webhook payloads from external services (e.g., Stripe)
    and tracks their processing status. It provides idempotency checking and
    retry capabilities for failed webhooks.

    Attributes:
        id: UUID primary key for the event
        provider: Identifier for the webhook source (e.g., 'stripe', 'stripe_connect')
        event_id: Unique event ID from the provider for idempotency
        payload: The full JSON payload received from the webhook
        status: Processing status of the webhook event
        received_at: Timestamp when the webhook was received
        processed_at: Timestamp when processing completed (null if not processed)
        error_message: Details of any processing errors
        retry_count: Number of times processing has been attempted

    Usage:
        # Check for duplicate events (idempotency)
        if WebhookEvent.objects.filter(provider='stripe', event_id=event_id).exists():
            return  # Already processed

        # Create new webhook event
        webhook_event = WebhookEvent.objects.create(
            provider='stripe',
            event_id=event_id,
            payload=payload_json,
            status=WebhookEventStatus.RECEIVED
        )

        # Process asynchronously
        process_webhook_event_task.delay(webhook_event.id)
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this webhook event"
    )
    provider = models.CharField(
        max_length=50,
        db_index=True,
        help_text=_("Identifier for the webhook source (e.g., 'stripe', 'paypal')")
    )
    event_id = models.CharField(
        max_length=255,
        help_text=_("Unique event ID from the provider for idempotency")
    )
    payload = models.JSONField(
        help_text=_("The full JSON payload received from the webhook")
    )
    status = models.CharField(
        max_length=20,
        choices=WebhookEventStatus.choices,
        default=WebhookEventStatus.RECEIVED,
        db_index=True,
        help_text=_("Processing status of the webhook event")
    )
    received_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Timestamp when webhook was received"
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text="Timestamp when processing completed"
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        help_text=_("Details of the error if processing failed")
    )
    retry_count = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of times processing has been attempted")
    )

    class Meta:
        ordering = ['-received_at']
        verbose_name = _("Webhook Event")
        verbose_name_plural = _("Webhook Events")
        # Ensure uniqueness for idempotency
        unique_together = [['provider', 'event_id']]
        indexes = [
            models.Index(fields=['provider', 'event_id']),
            models.Index(fields=['status', 'received_at']),
        ]

    def __str__(self):
        return f"{self.provider} - {self.event_id} ({self.status})"

    def mark_as_processing(self):
        """Mark the webhook event as currently being processed."""
        self.status = WebhookEventStatus.PROCESSING
        self.save(update_fields=['status'])

    def mark_as_processed(self):
        """Mark the webhook event as successfully processed."""
        self.status = WebhookEventStatus.PROCESSED
        self.processed_at = timezone.now()
        self.save(update_fields=['status', 'processed_at'])

    def mark_as_failed(self, error_message: str):
        """
        Mark the webhook event as failed.

        Args:
            error_message: Description of the failure
        """
        self.status = WebhookEventStatus.FAILED
        self.error_message = error_message
        self.retry_count += 1
        self.save(update_fields=['status', 'error_message', 'retry_count'])
