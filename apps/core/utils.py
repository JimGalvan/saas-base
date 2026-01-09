"""
Common utility functions for Django SaaS Starter.

Provides helper functions for working with environment variables and other common tasks.
"""
import os
from typing import Union, Optional


def get_env_int(key: str, default: Optional[int] = None) -> Optional[int]:
    """
    Get an integer value from environment variables.

    Args:
        key: The environment variable key
        default: Default value if key doesn't exist or value can't be converted

    Returns:
        Integer value or default if not found/invalid

    Example:
        >>> get_env_int('MAX_UPLOAD_SIZE', 5242880)
        5242880
    """
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


def get_env_float(key: str, default: Optional[float] = None) -> Optional[float]:
    """
    Get a float value from environment variables.

    Args:
        key: The environment variable key
        default: Default value if key doesn't exist or value can't be converted

    Returns:
        Float value or default if not found/invalid

    Example:
        >>> get_env_float('TAX_RATE', 0.08)
        0.08
    """
    try:
        return float(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


def get_env_number(
    key: str,
    default: Optional[Union[int, float]] = None
) -> Optional[Union[int, float]]:
    """
    Get a numeric value (int or float) from environment variables.
    Attempts to convert to int first, then float if that fails.

    Args:
        key: The environment variable key
        default: Default value if key doesn't exist or value can't be converted

    Returns:
        Numeric value (int or float) or default if not found/invalid

    Example:
        >>> get_env_number('THRESHOLD', 100)
        100
    """
    value = os.getenv(key)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return default


def get_env_bool(key: str, default: bool = False) -> bool:
    """
    Get a boolean value from environment variables.
    Recognizes: true, yes, 1, on (case-insensitive) as True

    Args:
        key: The environment variable key
        default: Default value if key doesn't exist

    Returns:
        Boolean value

    Example:
        >>> get_env_bool('DEBUG', False)
        False
    """
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ('true', 'yes', '1', 'on')
