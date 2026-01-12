"""
Maintenance Mode models for Django SaaS Starter.

This module provides a singleton model for managing site-wide maintenance mode,
allowing administrators to temporarily disable public access to the site.
"""
from django.db import models
from django.core.cache import cache


class MaintenanceMode(models.Model):
    """
    A singleton model to store maintenance mode settings.

    This model stores the maintenance mode state and custom message.
    Only one instance of this model should exist in the database.

    The model uses caching to avoid frequent database queries when
    checking if maintenance mode is active.

    Attributes:
        is_active: Boolean indicating if maintenance mode is enabled
        message: Custom message to display during maintenance
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    is_active = models.BooleanField(
        default=False,
        help_text="Enable maintenance mode site-wide"
    )
    message = models.TextField(
        default="We're currently making important updates to our site. Please check back soon!",
        help_text="Message to display during maintenance"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Maintenance Mode'
        verbose_name_plural = 'Maintenance Mode'

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance or create it if it doesn't exist.

        Returns:
            MaintenanceMode: The singleton instance
        """
        instance, created = cls.objects.get_or_create(pk=1)
        return instance

    @classmethod
    def is_maintenance_mode_active(cls):
        """
        Check if maintenance mode is active, with cache for performance.

        This method checks the cache first to avoid database queries on
        every request. The cache is automatically updated when the model
        is saved.

        Returns:
            bool: True if maintenance mode is active, False otherwise
        """
        # Try to get from cache first
        status = cache.get('maintenance_mode_active')

        if status is None:
            # If not in cache, get from database
            try:
                instance = cls.get_instance()
                status = instance.is_active
                # Cache for 60 seconds
                cache.set('maintenance_mode_active', status, 60)
            except:
                # Default to False if any error occurs
                status = False

        return status

    def save(self, *args, **kwargs):
        """
        Override save to update cache and enforce singleton pattern.

        Ensures only one instance exists and updates the cache whenever
        the model is saved.
        """
        # If this is a new instance and there's already another one, don't save
        if not self.pk and MaintenanceMode.objects.exists():
            return

        # Call the "real" save() method
        super().save(*args, **kwargs)

        # Update cache
        cache.set('maintenance_mode_active', self.is_active, 60)

    def __str__(self):
        """String representation showing current status."""
        status = "ACTIVE" if self.is_active else "INACTIVE"
        return f"Maintenance Mode: {status}"
