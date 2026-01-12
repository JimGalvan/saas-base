"""
Django admin configuration for accounts app.

This module configures the admin interface for User management.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for User model.

    Extends Django's UserAdmin to display UUID, timestamps,
    and subscription status in the admin interface.
    """

    list_display = [
        'email',
        'username',
        'is_active',
        'is_staff',
        'has_active_subscription',
        'created_at',
    ]

    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser',
        'created_at',
    ]

    search_fields = [
        'email',
        'username',
        'first_name',
        'last_name',
    ]

    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'last_login',
        'date_joined',
    ]

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
        ('System Info', {
            'fields': ('id',),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    ordering = ['-created_at']
