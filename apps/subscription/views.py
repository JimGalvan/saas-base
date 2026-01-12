"""
Subscription views for Django SaaS Starter.

This module provides views for managing subscriptions, Stripe checkout,
and subscription status pages.

TODO: Implement subscription views based on your requirements:
- Subscription detail/dashboard view
- Create Stripe checkout session
- Manage subscription (update/cancel)
- Success/cancel pages
- Webhook handlers for Stripe events

Example implementation:

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import stripe
from django.conf import settings
from apps.subscription.models import Customer, Subscription
from apps.subscription.utils import sync_subscription_status_and_plan

@login_required
def subscription_detail(request):
    '''Display user's current subscription details.'''
    try:
        customer = request.user.customer
        subscription = customer.subscription_set.first()
        context = {
            'subscription': subscription,
            'is_active': subscription.is_active if subscription else False,
        }
    except Customer.DoesNotExist:
        context = {
            'subscription': None,
            'is_active': False,
        }
    return render(request, 'subscription/detail.html', context)

@login_required
def create_checkout_session(request):
    '''Create a Stripe Checkout session for subscription.'''
    stripe.api_key = settings.STRIPE_API_KEY

    # Get or create customer
    customer, created = Customer.objects.get_or_create(user=request.user)

    if not customer.stripe_customer_id:
        stripe_customer = stripe.Customer.create(email=request.user.email)
        customer.stripe_customer_id = stripe_customer.id
        customer.save()

    # Create checkout session
    checkout_session = stripe.checkout.Session.create(
        customer=customer.stripe_customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price': settings.STRIPE_PRICE_ID,  # Your price ID
            'quantity': 1,
        }],
        mode='subscription',
        success_url=request.build_absolute_uri('/subscription/success/'),
        cancel_url=request.build_absolute_uri('/subscription/cancel/'),
    )

    return redirect(checkout_session.url)
"""
from django.shortcuts import render

# Create your views here.
# Implement your subscription views here
