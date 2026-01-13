"""
Django admin configuration for webhooks app.

This module configures the admin interface for viewing and managing
webhook events from external services.
"""
from django.contrib import admin
from django.utils.html import format_html
from apps.webhooks.models import WebhookEvent, WebhookEventStatus


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    """
    Admin interface for WebhookEvent model.

    Provides a read-only view of webhook events with filtering
    and search capabilities for debugging webhook issues.
    """
    list_display = [
        'provider',
        'event_id',
        'status_badge',
        'received_at',
        'processed_at',
        'retry_count'
    ]

    list_filter = [
        'provider',
        'status',
        'received_at'
    ]

    search_fields = [
        'event_id',
        'payload',
        'error_message'
    ]

    readonly_fields = [
        'id',
        'provider',
        'event_id',
        'payload',
        'received_at',
        'processed_at',
        'status',
        'error_message',
        'retry_count'
    ]

    ordering = ['-received_at']

    fieldsets = (
        ('Event Information', {
            'fields': ('provider', 'event_id', 'status', 'retry_count')
        }),
        ('Payload', {
            'fields': ('payload',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('received_at', 'processed_at')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('System Info', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        """
        Display status with color-coded badges.

        Args:
            obj: The WebhookEvent instance

        Returns:
            str: HTML formatted status badge
        """
        colors = {
            WebhookEventStatus.RECEIVED: '#3498db',  # Blue
            WebhookEventStatus.PROCESSING: '#f39c12',  # Orange
            WebhookEventStatus.PROCESSED: '#2ecc71',  # Green
            WebhookEventStatus.FAILED: '#e74c3c',  # Red
        }
        color = colors.get(obj.status, '#95a5a6')  # Default gray

        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def has_add_permission(self, request):
        """
        Prevent manual creation of webhook events.

        Webhook events should only be created by the webhook handlers.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Allow deletion of old webhook events for cleanup.

        Returns:
            bool: True (allow deletion)
        """
        return True
