"""
URL patterns for webhooks app.

This module defines URL patterns for webhook endpoints from external services.
"""
from django.urls import path
from . import handlers

app_name = 'webhooks'

urlpatterns = [
    # Stripe webhooks
    path('stripe/account/', handlers.account_webhook_router, name='stripe_account'),
    path('stripe/connect/', handlers.connect_webhook_router, name='stripe_connect'),

    # Add more webhook endpoints as needed
    # path('paypal/', handlers.paypal_webhook_router, name='paypal'),
    # path('github/', handlers.github_webhook_router, name='github'),
]
