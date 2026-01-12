"""
URL patterns for subscription app.

This module defines URL patterns for subscription-related views including
subscription management, Stripe checkout, and webhook handling.
"""
from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    # Subscription management views will be implemented as needed
    # Examples:
    # path('', views.subscription_detail, name='detail'),
    # path('checkout/', views.create_checkout_session, name='checkout'),
    # path('manage/', views.manage_subscription, name='manage'),
    # path('cancel/', views.cancel_subscription, name='cancel'),
    # path('success/', views.subscription_success, name='success'),
]
