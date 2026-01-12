"""
Django admin configuration for subscription app.

This module configures the admin interface for Customer and Subscription models.
"""
from django.contrib import admin
from apps.subscription.models import Customer, Subscription


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin interface for Customer model.

    Displays customer information and their Stripe customer ID.
    """
    list_display = [
        'user',
        'stripe_customer_id',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'user__email',
        'user__username',
        'stripe_customer_id',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
    ]

    list_filter = [
        'created_at',
    ]

    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'stripe_customer_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('System Info', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin interface for Subscription model.

    Displays subscription details including plan, status, and payment information.
    """
    list_display = [
        'customer',
        'plan',
        'status',
        'is_active',
        'stripe_subscription_id',
        'created_at',
    ]

    list_filter = [
        'plan',
        'status',
        'created_at',
    ]

    search_fields = [
        'customer__user__email',
        'customer__user__username',
        'stripe_subscription_id',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'is_active',
    ]

    fieldsets = (
        ('Subscription Information', {
            'fields': ('customer', 'stripe_subscription_id', 'plan', 'status')
        }),
        ('Payment Information', {
            'fields': ('last_payment_status',)
        }),
        ('Status', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('System Info', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    def is_active(self, obj):
        """Display whether subscription is active."""
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = 'Active'
