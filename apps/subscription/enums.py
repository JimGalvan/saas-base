"""
Subscription enums for Django SaaS Starter.

This module defines enumerations for subscription statuses and plan types
used throughout the subscription system.
"""
from django.db import models


class SubscriptionStatus(models.TextChoices):
    """
    Stripe subscription status values.

    These statuses are used to track the current state of a subscription
    and correspond to Stripe's subscription status values.
    """
    ACTIVE = "active", "Active"
    TRIALING = "trialing", "Trialing"
    PAST_DUE = "past_due", "Past Due"
    CANCELED = "canceled", "Canceled"
    UNPAID = "unpaid", "Unpaid"
    INCOMPLETE = "incomplete", "Incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired", "Incomplete Expired"
    # Custom status for subscriptions not created in Stripe
    NO_SUBSCRIPTION = "no_subscription", "No Subscription"


class PlanType(models.TextChoices):
    """
    Subscription plan types.

    Define the available subscription tiers for your SaaS.
    These can be customized based on your pricing model.
    """
    FREE = "free", "Free"
    PLUS = "plus", "Plus"
    UNKNOWN = "unknown", "Unknown"
