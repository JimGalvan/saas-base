"""
URL configuration for Django SaaS Starter.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Core pages
    path('', include('apps.core.urls')),

    # Authentication (django-allauth)
    path('accounts/', include('allauth.urls')),

    # Webhooks
    path('webhooks/', include('apps.webhooks.urls')),

    # Subscription URLs (add when views are created)
    # path('subscription/', include('apps.subscription.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
