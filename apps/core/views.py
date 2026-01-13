"""
Core views for Django SaaS Starter.

This module provides basic views for home, dashboard, and legal pages.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    """Home page view."""
    return render(request, 'home.html')


@login_required
def dashboard(request):
    """User dashboard view."""
    return render(request, 'dashboard.html')


def privacy_policy(request):
    """Privacy policy page."""
    return render(request, 'legal/privacy.html')


def terms_of_service(request):
    """Terms of service page."""
    return render(request, 'legal/terms.html')
