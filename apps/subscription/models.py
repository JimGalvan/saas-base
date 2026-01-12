"""
Subscription models for Django SaaS Starter.

This module provides models for managing Stripe subscriptions and customers.
"""
from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.subscription.enums import SubscriptionStatus, PlanType


class Customer(BaseModel):
    """
    Customer model for Stripe integration.

    Links a Django user to their Stripe customer ID. This model stores
    the Stripe customer identifier and provides a one-to-one relationship
    with the user model.

    Attributes:
        user: One-to-one relationship with the User model
        stripe_customer_id: The customer ID from Stripe
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer',
        help_text="User associated with this customer"
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text="Stripe customer ID"
    )

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"Customer for {self.user.email}"


class Subscription(BaseModel):
    """
    Subscription model for tracking user subscriptions.

    Stores subscription information synchronized with Stripe. This model
    tracks the subscription status, plan type, and payment information.

    Attributes:
        customer: Foreign key to Customer model
        stripe_subscription_id: The subscription ID from Stripe
        plan: The subscription plan type (FREE, PLUS, etc.)
        status: Current subscription status
        last_payment_status: Status of the last payment attempt
    """
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Customer associated with this subscription"
    )
    stripe_subscription_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Stripe subscription ID"
    )
    plan = models.CharField(
        max_length=50,
        choices=PlanType.choices,
        default=PlanType.FREE,
        help_text="Subscription plan type"
    )
    status = models.CharField(
        max_length=50,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.NO_SUBSCRIPTION,
        help_text="Current subscription status"
    )
    last_payment_status = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Status of the last payment"
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f"{self.customer.user.email} - {self.plan} ({self.status})"

    @property
    def is_active(self):
        """Check if subscription is currently active."""
        return self.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]
