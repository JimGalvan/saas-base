"""
Django-allauth adapters for Django SaaS Starter.

This module provides custom adapters to customize django-allauth behavior
for user authentication and account management.
"""
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings


class AccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter for django-allauth.

    This adapter allows customization of authentication behavior such as:
    - Email verification requirements
    - Redirect URLs after login/signup
    - User save behavior
    - Password validation

    Usage:
        Configure in settings.py:
        ACCOUNT_ADAPTER = 'apps.accounts.adapters.AccountAdapter'
    """

    def is_open_for_signup(self, request):
        """
        Check if the site is open for new signups.

        This can be used to temporarily disable new user registrations
        or implement invitation-only signups.

        Args:
            request: The HTTP request object

        Returns:
            bool: True if signups are allowed, False otherwise
        """
        # You can add custom logic here, e.g., check a site-wide setting
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def get_login_redirect_url(self, request):
        """
        Get the URL to redirect to after successful login.

        Args:
            request: The HTTP request object

        Returns:
            str: The redirect URL
        """
        # Default to home page, but you can customize based on user type
        # For example, redirect to dashboard for authenticated users
        if request.user.is_authenticated:
            return getattr(settings, 'LOGIN_REDIRECT_URL', '/')
        return super().get_login_redirect_url(request)

    def save_user(self, request, user, form, commit=True):
        """
        Save a newly created user.

        This method is called when a new user signs up. You can customize
        it to set additional fields or perform actions on user creation.

        Args:
            request: The HTTP request object
            user: The user instance being created
            form: The signup form
            commit: Whether to save the user to the database

        Returns:
            User: The user instance
        """
        user = super().save_user(request, user, form, commit=False)

        # You can add custom logic here, e.g., set additional fields
        # user.custom_field = some_value

        if commit:
            user.save()

        return user
