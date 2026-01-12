"""
Django admin configuration for maintenance app.

This module configures the admin interface for the MaintenanceMode singleton model,
allowing administrators to easily toggle maintenance mode on/off.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import MaintenanceMode


@admin.register(MaintenanceMode)
class MaintenanceModeAdmin(admin.ModelAdmin):
    """
    Admin interface for MaintenanceMode model.

    Provides a simple interface to toggle maintenance mode and customize
    the maintenance message. The interface includes:
    - Visual status indicators with color coding
    - Message preview in list view
    - Warnings about the impact of enabling maintenance mode
    - Prevents multiple instances (singleton pattern)
    """
    list_display = ['maintenance_status', 'message_preview', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('is_active', 'message'),
            'description': '<div class="help" style="margin-bottom: 15px; padding: 10px; background-color: #f8f8f8; border-left: 4px solid #79aec8;">'
                           '<strong>Warning:</strong> Enabling maintenance mode will make the site unavailable to regular users. '
                           'Only admin pages and staff users will remain accessible.</div>'
        }),
        ('History', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def maintenance_status(self, obj):
        """
        Display maintenance status with color indicators.

        Args:
            obj: The MaintenanceMode instance

        Returns:
            str: HTML formatted status string
        """
        if obj.is_active:
            return format_html(
                '<span style="color: #e74c3c; font-weight: bold;">✘ ACTIVE</span>'
            )
        return format_html(
            '<span style="color: #2ecc71;">✓ INACTIVE</span>'
        )
    maintenance_status.short_description = 'Status'

    def message_preview(self, obj):
        """
        Show a preview of the maintenance message.

        Args:
            obj: The MaintenanceMode instance

        Returns:
            str: Truncated message preview
        """
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    message_preview.short_description = 'Message'

    def has_add_permission(self, request):
        """
        Prevent creating additional instances.

        Returns:
            bool: False if instance exists, True otherwise
        """
        return not MaintenanceMode.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of the singleton instance.

        Returns:
            bool: Always False
        """
        return False
