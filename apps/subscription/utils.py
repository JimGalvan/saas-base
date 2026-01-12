"""
Subscription utilities for Django SaaS Starter.

This module provides helper functions for managing Stripe subscriptions,
checking subscription status, and syncing data with Stripe.
"""
import stripe
from django.conf import settings

from apps.subscription.enums import SubscriptionStatus, PlanType
from apps.subscription.models import Subscription


def get_enum_by_value(value):
    """
    Get a SubscriptionStatus enum member by its value.

    Args:
        value: The string value to search for

    Returns:
        SubscriptionStatus member or None if not found
    """
    for member in SubscriptionStatus:
        if member.value == value:
            return member
    return None


def get_enum_label(value, enum):
    """
    Get the display label for an enum value.

    Args:
        value: The enum value
        enum: The enum class to search in

    Returns:
        str: The label for the enum value or None if not found
    """
    for member in enum:
        if member.value == value:
            return member.label
    return None


def is_subscription_not_active(current_subscription_status):
    """
    Check if a subscription status indicates an inactive subscription.

    Args:
        current_subscription_status: The SubscriptionStatus to check

    Returns:
        bool: True if subscription is not active, False otherwise
    """
    inactive_statuses = [
        SubscriptionStatus.NO_SUBSCRIPTION,
        SubscriptionStatus.CANCELED,
        SubscriptionStatus.UNPAID,
        SubscriptionStatus.INCOMPLETE,
        SubscriptionStatus.INCOMPLETE_EXPIRED,
        SubscriptionStatus.PAST_DUE,
    ]
    return current_subscription_status in inactive_statuses


def get_plan_type(subscription: Subscription) -> PlanType:
    """
    Determine the plan type based on subscription status.

    Args:
        subscription: The Subscription instance

    Returns:
        PlanType: The determined plan type (FREE, PLUS, or UNKNOWN)
    """
    current_subscription_status = subscription.status

    if current_subscription_status == SubscriptionStatus.ACTIVE:
        return PlanType.PLUS
    elif is_subscription_not_active(current_subscription_status):
        return PlanType.FREE
    else:
        return PlanType.UNKNOWN


def sync_subscription_plan(subscription: Subscription) -> Subscription:
    """
    Synchronize the subscription plan based on its status.

    Args:
        subscription: The Subscription instance to sync

    Returns:
        Subscription: The updated subscription instance
    """
    plan = get_plan_type(subscription)
    subscription.plan = plan
    subscription.save()
    return subscription


def sync_subscription_status_and_plan(subscription: Subscription) -> Subscription:
    """
    Sync subscription status and plan with Stripe.

    Retrieves the latest subscription data from Stripe and updates
    the local subscription record.

    Args:
        subscription: The Subscription instance to sync

    Returns:
        Subscription: The updated subscription instance

    Raises:
        ValueError: If subscription doesn't have a Stripe subscription ID
        stripe.error.StripeError: If there's an error communicating with Stripe
    """
    stripe_subscription_id = subscription.stripe_subscription_id
    if not stripe_subscription_id:
        raise ValueError("Subscription does not have a Stripe subscription ID.")

    # Ensure Stripe API key is set
    stripe.api_key = settings.STRIPE_API_KEY

    # Retrieve subscription from Stripe
    stripe_subscription = stripe.Subscription.retrieve(stripe_subscription_id)
    subscription_status = stripe_subscription["status"]

    # Update local subscription
    subscription.status = get_enum_by_value(subscription_status)
    subscription = sync_subscription_plan(subscription)

    return subscription
