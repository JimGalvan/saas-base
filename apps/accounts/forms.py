"""
Authentication forms for Django SaaS Starter.

This module provides customized forms for user authentication
including reCAPTCHA integration for signup and improved error messages for login.
"""
from allauth.account.forms import SignupForm, LoginForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.conf import settings
from django.forms import ValidationError


class CaptchaSignupForm(SignupForm):
    """
    Custom signup form with reCAPTCHA integration.

    Extends django-allauth's SignupForm to add bot protection via Google reCAPTCHA.
    The reCAPTCHA field is only added if DISABLE_RECAPTCHA setting is False.

    Usage:
        Configure in settings.py:
        ACCOUNT_FORMS = {
            'signup': 'apps.accounts.forms.CaptchaSignupForm',
        }
    """
    # Use the checkbox version of reCAPTCHA which is more visible
    if not getattr(settings, 'DISABLE_RECAPTCHA', False):
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def save(self, request):
        """
        Save the user account.

        Args:
            request: The HTTP request object

        Returns:
            User: The created user instance
        """
        user = super(CaptchaSignupForm, self).save(request)
        return user


class CustomLoginForm(LoginForm):
    """
    Custom login form with improved error messages.

    Extends django-allauth's LoginForm to provide more user-friendly
    error messages that don't reveal whether an account exists.

    Usage:
        Configure in settings.py:
        ACCOUNT_FORMS = {
            'login': 'apps.accounts.forms.CustomLoginForm',
        }
    """
    error_messages = {
        "account_inactive": "This account is currently inactive. Please check your email for verification instructions.",
        "email_password_mismatch": "The email or password you entered is incorrect. Please try again.",
        "username_password_mismatch": "The email or password you entered is incorrect. Please try again.",
    }

    def clean(self):
        """
        Validate the login credentials.

        Returns:
            dict: The cleaned form data

        Raises:
            ValidationError: If credentials are invalid
        """
        try:
            cleaned_data = super().clean()
            return cleaned_data
        except ValidationError as e:
            # Replace generic error messages with more user-friendly ones
            if 'email/password' in str(e) or 'username/password' in str(e):
                raise ValidationError(self.error_messages["email_password_mismatch"])
            raise
