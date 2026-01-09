"""
Middleware classes for Django SaaS Starter.

Provides reusable middleware for:
- Maintenance mode with admin exemptions
- Translation/i18n debugging
- Firebase service worker stub handling
"""
import re
import logging
from django.shortcuts import render
from django.conf import settings
from django.utils.translation import activate
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class MaintenanceModeMiddleware:
    """
    Middleware to check if the site is in maintenance mode.

    Displays maintenance page when active, with exemptions for:
    - Staff/admin users
    - Admin panel (/admin/)
    - Static files
    - Media files
    - Maintenance endpoints
    - Login page

    The maintenance status is retrieved from the database via the
    MaintenanceMode model (will be created in Phase 5).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Define excluded URL patterns
        self.excluded_urls = [
            r'^/admin/',
            r'^/static/',
            r'^/media/',
            r'^/maintenance/',
            r'^/accounts/login/',
        ]

    def __call__(self, request):
        # Staff/admin users bypass maintenance mode
        if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)

        # Check if maintenance mode is active
        try:
            from apps.maintenance.models import MaintenanceMode
            maintenance_mode = MaintenanceMode.is_maintenance_mode_active()
        except:
            # Fallback to settings if database query fails
            maintenance_mode = getattr(settings, 'MAINTENANCE_MODE', False)

        if maintenance_mode:
            # Check if current URL should be excluded
            path = request.path_info.lstrip('/')
            full_path = f'/{path}'

            for url_pattern in self.excluded_urls:
                if re.search(url_pattern, full_path):
                    return self.get_response(request)

            # Get customized message
            try:
                from apps.maintenance.models import MaintenanceMode
                message = MaintenanceMode.get_instance().message
            except:
                message = "We're currently making important updates. Please check back soon!"

            # HTMX requests get simplified response
            if request.headers.get('HX-Request'):
                return render(
                    request,
                    'maintenance/maintenance_htmx.html',
                    {'message': message},
                    status=503
                )

            # All other requests get full maintenance page
            return render(
                request,
                'maintenance/maintenance.html',
                {'message': message},
                status=503
            )

        return self.get_response(request)


class TranslationDebugMiddleware(MiddlewareMixin):
    """
    Middleware to ensure translations are loaded correctly.

    Useful for debugging i18n issues in development. Activates the proper
    language based on session/cookie and adds debug headers in development mode.
    """

    def process_request(self, request):
        """Ensure proper language activation."""
        # Get language from session, cookie, or default
        language = (
            request.session.get('_language') or
            request.COOKIES.get('django_language') or
            request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME) or
            settings.LANGUAGE_CODE
        )

        # Activate the language
        if language:
            activate(language)

        # Debug log
        if settings.DEBUG:
            logger.debug(f"Active language: {language}")

        return None

    def process_response(self, request, response):
        """Add language debugging headers in development."""
        if settings.DEBUG:
            language = getattr(request, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
            response['X-Language'] = language
        return response


class FirebaseMiddleware:
    """
    Middleware that handles requests to Firebase service worker.

    Returns 204 No Content to prevent 404 errors for Firebase messaging
    service worker requests when Firebase is not actively being used.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/firebase-messaging-sw.js':
            from django.http import HttpResponse
            return HttpResponse(status=204)
        return self.get_response(request)
