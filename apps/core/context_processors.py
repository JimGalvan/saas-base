"""
Context processors for Django SaaS Starter.

These functions add variables to the template context automatically,
making them available in all templates without explicitly passing them.
"""
from django.conf import settings


def environment(request):
    """
    Add environment variables to template context.

    Makes environment information available for conditional rendering
    in templates (e.g., showing banners in dev/qa).

    Returns:
        dict: Context variables including DEBUG, ENV, BASE_URL
    """
    return {
        'DEBUG': settings.DEBUG,
        'ENV': getattr(settings, 'ENV', 'development'),
        'BASE_URL': getattr(settings, 'BASE_URL', 'http://localhost:8000'),
    }


def recaptcha(request):
    """
    Add reCAPTCHA configuration to template context.

    Makes reCAPTCHA site key and enable/disable flag available
    in templates for form rendering.

    Returns:
        dict: reCAPTCHA public key and enabled flag
    """
    return {
        'RECAPTCHA_SITE_KEY': getattr(settings, 'RECAPTCHA_PUBLIC_KEY', ''),
        'RECAPTCHA_ENABLED': not getattr(settings, 'DISABLE_RECAPTCHA', False),
    }


def user_subscription(request):
    """
    Add user subscription status to template context.

    Safely retrieves subscription information for authenticated users.
    Only adds data for users with subscriptions. Fails gracefully if
    subscription app is not yet configured.

    Returns:
        dict: Subscription status variables
    """
    if not request.user.is_authenticated:
        return {}

    try:
        # Try to get subscription from user
        # This will be available after Phase 4 when subscription app is added
        subscription = request.user.customer.subscription_set.first()
        if subscription:
            return {
                'user_subscription': subscription,
                'has_active_subscription': subscription.is_active,
            }
    except:
        # Subscription app not yet configured or user has no customer record
        pass

    return {
        'user_subscription': None,
        'has_active_subscription': False,
    }
