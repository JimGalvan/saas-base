"""
Core models for Django SaaS Starter.

This module provides abstract base models that can be used throughout the application.
"""
import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model for all models in the application.

    Provides UUID primary key and automatic timestamp tracking.
    All models inheriting from this will have:
    - UUID primary key (better for distributed systems and security)
    - created_at: Timestamp when record was created
    - updated_at: Timestamp when record was last updated
    - Default ordering by creation date (newest first)

    Usage:
        class YourModel(BaseModel):
            # Your fields here
            name = models.CharField(max_length=100)
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this record"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when this record was last updated"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        """Default string representation showing class name and ID."""
        return f"{self.__class__.__name__} {self.id}"
