"""
Webhook handlers for Django SaaS Starter.

This module provides webhook routers for handling incoming webhooks from
external services like Stripe. Includes signature verification, idempotency
checking, and asynchronous processing.
"""
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import stripe
from django.conf import settings

from apps.webhooks.models import WebhookEvent, WebhookEventStatus

logger = logging.getLogger(__name__)

# Stripe configuration
stripe.api_key = getattr(settings, 'STRIPE_API_KEY', '')
STRIPE_ACCOUNT_WEBHOOK_SECRET = getattr(settings, 'STRIPE_ACCOUNT_WEBHOOK_SECRET', '')
STRIPE_CONNECT_WEBHOOK_SECRET = getattr(settings, 'STRIPE_CONNECT_WEBHOOK_SECRET', '')


@csrf_exempt
def account_webhook_router(request):
    """
    Router for account-level Stripe webhook events.

    Handles webhook events from the main Stripe account (e.g., subscriptions).
    This function:
    1. Validates the webhook signature
    2. Checks for duplicate events (idempotency)
    3. Stores the event in the database
    4. Enqueues it for asynchronous processing (optional)
    5. Returns a 200 OK response to acknowledge receipt

    Args:
        request: The HTTP request containing the webhook payload

    Returns:
        HttpResponse: 200 OK if successful, 400 if invalid

    Note:
        In DEBUG mode, unsigned webhooks are accepted for local testing.
        In production, signature verification is mandatory.

    Usage:
        Add to your urls.py:
        path('webhooks/stripe/account/', account_webhook_router, name='stripe_account_webhook'),
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    event_id = None
    payload_json = None
    provider = 'stripe'

    # --- 1. Validate and Parse Webhook ---
    try:
        # Attempt to parse payload first for logging ID if verification fails
        try:
            payload_json = json.loads(payload)
            event_id = payload_json.get('id')
        except json.JSONDecodeError:
            logger.warning("Account webhook received non-JSON payload.")
            # Continue to signature check if header exists

        if sig_header and STRIPE_ACCOUNT_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_ACCOUNT_WEBHOOK_SECRET
            )
            # If construct_event succeeds, use its parsed payload
            payload_json = event  # It's already a dict-like object
            event_id = event.id
            logger.info(f"Account webhook signature verified for event: {event_id}")
        elif settings.DEBUG:  # Allow unsigned events in DEBUG mode ONLY
            if not payload_json:
                raise ValueError("Cannot parse payload in DEBUG mode without signature.")
            event_id = payload_json.get('id')
            logger.warning(f"Processing unsigned account webhook in DEBUG mode: {event_id}")
        else:
            raise ValueError("Missing signature and not in DEBUG mode")

        if not event_id:
            raise ValueError("Could not determine event ID from webhook payload")

    except ValueError as e:
        # Invalid payload
        logger.error(f"Account webhook error parsing payload: {e}. Event ID from JSON: {event_id}", exc_info=True)
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Account webhook signature verification failed: {e}. Event ID from JSON: {event_id}", exc_info=True)
        return HttpResponseBadRequest("Invalid signature")
    except Exception as e:
        logger.error(f"Unexpected error processing account webhook header/signature: {e}. Event ID from JSON: {event_id}", exc_info=True)
        return HttpResponseBadRequest("Error processing webhook")

    # --- 2. Idempotency Check ---
    if WebhookEvent.objects.filter(provider=provider, event_id=event_id).exists():
        logger.info(f"Duplicate account webhook event received: {provider} - {event_id}. Skipping.")
        return HttpResponse(status=200)

    # --- 3. Store Raw Event ---
    try:
        webhook_event = WebhookEvent.objects.create(
            provider=provider,
            event_id=event_id,
            payload=payload_json,  # Store the parsed JSON/event object
            status=WebhookEventStatus.RECEIVED
        )
        logger.info(f"Stored WebhookEvent {webhook_event.id} for account event {event_id}")
    except Exception as e:
        logger.error(f"Failed to save WebhookEvent for account event {event_id}: {e}", exc_info=True)
        return HttpResponse("Internal server error storing webhook event", status=500)

    # --- 4. Enqueue Task (Optional) ---
    # Uncomment and implement if you want async processing with Celery
    # try:
    #     from apps.webhooks.tasks import process_webhook_event_task
    #     process_webhook_event_task.delay(webhook_event.id)
    #     logger.info(f"Enqueued process_webhook_event_task for WebhookEvent {webhook_event.id}")
    # except Exception as e:
    #     logger.error(f"Failed to enqueue Celery task for WebhookEvent {webhook_event.id}: {e}", exc_info=True)
    #     webhook_event.mark_as_failed(f"Failed to enqueue Celery task: {e}")
    #     # Still return 200 to Stripe, event is stored.

    # --- 5. Return Success ---
    return HttpResponse(status=200)


@csrf_exempt
def connect_webhook_router(request):
    """
    Router for Connect account webhook events.

    Handles webhook events from connected Stripe accounts (e.g., for marketplaces).
    This function:
    1. Validates the webhook signature using Connect webhook secret
    2. Checks for duplicate events (idempotency)
    3. Stores the event in the database with 'stripe_connect' provider
    4. Enqueues it for asynchronous processing (optional)
    5. Returns a 200 OK response to acknowledge receipt

    Args:
        request: The HTTP request containing the webhook payload

    Returns:
        HttpResponse: 200 OK if successful, 400 if invalid

    Note:
        In DEBUG mode, unsigned webhooks are accepted for local testing.
        In production, signature verification is mandatory.

    Usage:
        Add to your urls.py:
        path('webhooks/stripe/connect/', connect_webhook_router, name='stripe_connect_webhook'),
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    event_id = None
    payload_json = None
    provider = 'stripe_connect'  # Differentiate provider

    # --- 1. Validate and Parse Webhook ---
    try:
        # Attempt to parse payload first for logging ID if verification fails
        try:
            payload_json = json.loads(payload)
            event_id = payload_json.get('id')
        except json.JSONDecodeError:
            logger.warning("Connect webhook received non-JSON payload.")
            # Continue to signature check if header exists

        if sig_header and STRIPE_CONNECT_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(
                payload, sig_header, STRIPE_CONNECT_WEBHOOK_SECRET
            )
            payload_json = event
            event_id = event.id
            logger.info(f"Connect webhook signature verified for event: {event_id}")
        elif settings.DEBUG:
            if not payload_json:
                raise ValueError("Cannot parse payload in DEBUG mode without signature.")
            event_id = payload_json.get('id')
            logger.warning(f"Processing unsigned Connect webhook in DEBUG mode: {event_id}")
        else:
            raise ValueError("Missing signature and not in DEBUG mode")

        if not event_id:
            raise ValueError("Could not determine event ID from webhook payload")

    except ValueError as e:
        logger.error(f"Connect webhook error parsing payload: {e}. Event ID from JSON: {event_id}", exc_info=True)
        return HttpResponseBadRequest("Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Connect webhook signature verification failed: {e}. Event ID from JSON: {event_id}", exc_info=True)
        return HttpResponseBadRequest("Invalid signature")
    except Exception as e:
        logger.error(f"Unexpected error processing Connect webhook header/signature: {e}. Event ID from JSON: {event_id}", exc_info=True)
        return HttpResponseBadRequest("Error processing webhook")

    # --- 2. Idempotency Check ---
    if WebhookEvent.objects.filter(provider=provider, event_id=event_id).exists():
        logger.info(f"Duplicate Connect webhook event received: {provider} - {event_id}. Skipping.")
        return HttpResponse(status=200)

    # --- 3. Store Raw Event ---
    try:
        webhook_event = WebhookEvent.objects.create(
            provider=provider,
            event_id=event_id,
            payload=payload_json,
            status=WebhookEventStatus.RECEIVED
        )
        logger.info(f"Stored WebhookEvent {webhook_event.id} for Connect event {event_id}")
    except Exception as e:
        logger.error(f"Failed to save WebhookEvent for Connect event {event_id}: {e}", exc_info=True)
        return HttpResponse("Internal server error storing webhook event", status=500)

    # --- 4. Enqueue Task (Optional) ---
    # Uncomment and implement if you want async processing with Celery
    # try:
    #     from apps.webhooks.tasks import process_webhook_event_task
    #     process_webhook_event_task.delay(webhook_event.id)
    #     logger.info(f"Enqueued process_webhook_event_task for WebhookEvent {webhook_event.id}")
    # except Exception as e:
    #     logger.error(f"Failed to enqueue Celery task for WebhookEvent {webhook_event.id}: {e}", exc_info=True)
    #     webhook_event.mark_as_failed(f"Failed to enqueue Celery task: {e}")

    # --- 5. Return Success ---
    return HttpResponse(status=200)
