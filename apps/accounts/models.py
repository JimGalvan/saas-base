"""
User models for Django SaaS Starter.

This module provides a custom User model with UUID primary key
and subscription integration.
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with UUID primary key and subscription integration.

    Extends Django's AbstractUser to use UUID instead of auto-increment ID
    for better distributed system support and security.

    Features:
    - UUID primary key for security and scalability
    - Timestamp tracking (created_at, updated_at)
    - Subscription status checking methods
    - Email-based authentication (via django-allauth)
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
        """Return email or username as string representation."""
        return self.email or self.username

    def has_active_subscription(self):
        """
        Check if the user currently has an active subscription.

        Returns:
            bool: True if user has active subscription, False otherwise

        Note:
            This method assumes a related 'customer' object with subscriptions.
            Requires the subscription app to be properly configured.
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

        Returns:
            bool: True if user has/had subscription

        Note:
            Currently checks only current status, but can be expanded
            to check subscription history if that data is available.
        """
        # For now, we're only checking current subscription status
        # In the future, this could be expanded to check a subscription history table
        return self.has_active_subscription()
